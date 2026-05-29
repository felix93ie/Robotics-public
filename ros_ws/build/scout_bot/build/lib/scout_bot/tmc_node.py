import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleStatus, VehicleLocalPosition
import math
import time
import yaml
from enum import Enum
from ament_index_python.packages import get_package_share_directory
import os

class TacticalState(Enum):
    INIT = 0
    ARM_AND_TAKEOFF = 1
    MOVE_TO_PHASE_LINE = 2
    OCCUPY_OP = 3
    HOLD_AT_OP = 4
    MOVE_TO_SCREEN_LINE = 5
    RBF = 6
    RTL = 7

class MissionWaypoint:
    def __init__(self, x, y, z, label, hold_seconds=0):
        self.x = x
        self.y = y
        self.z = z
        self.label = label
        self.hold_seconds = hold_seconds

class TMCNode(Node):
    def __init__(self):
        super().__init__('tmc_node')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Publishers
        self.offboard_control_mode_publisher = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_setpoint_publisher = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.vehicle_command_publisher = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos_profile)
        
        # Subscribers
        self.vehicle_status_subscriber = self.create_subscription(VehicleStatus, '/fmu/out/vehicle_status_v4', self.vehicle_status_callback, qos_profile)
        self.vehicle_local_position_subscriber = self.create_subscription(VehicleLocalPosition, '/fmu/out/vehicle_local_position_v1', self.vehicle_local_position_callback, qos_profile)
        
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz
        
        self.state = TacticalState.INIT
        self.vehicle_status = VehicleStatus()
        self.local_position = VehicleLocalPosition()
        self.status_received = False
        self.position_received = False
        
        self.load_mission_config()
        
        self.current_wp_index = 0
        self.mission_waypoints = []
        self.setup_mission()
        
        self.state_start_time = 0.0
        
        self.get_logger().info("TMC Node Initialized. State: INIT")

    def load_mission_config(self):
        try:
            package_share_directory = get_package_share_directory('scout_bot')
            config_path = os.path.join(package_share_directory, 'config', 'mission_config.yaml')
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.get_logger().info(f"Loaded mission config from {config_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to load mission config: {e}")
            # Fallback config
            self.config = {
                'patrol_altitude': -12.0,
                'screen_line': [
                    {'x': 0.0, 'y': 0.0, 'label': 'SP'},
                    {'x': 50.0, 'y': 0.0, 'label': 'PL Alpha'}
                ],
                'observation_points': [
                    {'x': 50.0, 'y': 30.0, 'label': 'OP 1', 'hold_seconds': 15}
                ]
            }

    def setup_mission(self):
        alt = self.config.get('patrol_altitude', -12.0)
        # Sequence: PL Alpha -> OP 1 -> RTL
        # Build the waypoint sequence based on config
        for sl in self.config.get('screen_line', []):
            self.mission_waypoints.append(MissionWaypoint(sl['x'], sl['y'], alt, sl['label']))
        for op in self.config.get('observation_points', []):
            self.mission_waypoints.append(MissionWaypoint(op['x'], op['y'], alt, op['label'], op.get('hold_seconds', 0)))

    def vehicle_status_callback(self, msg):
        self.vehicle_status = msg
        self.status_received = True

    def vehicle_local_position_callback(self, msg):
        self.local_position = msg
        self.position_received = True

    def timer_callback(self):
        if not self.status_received or not self.position_received:
            return
            
        self.publish_offboard_control_mode()
        
        if self.state == TacticalState.INIT:
            # Wait until ready to arm
            if self.vehicle_status.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
                self.transition_to(TacticalState.ARM_AND_TAKEOFF)
            else:
                self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0) # Custom mode, offboard
                self.arm()
                self.transition_to(TacticalState.ARM_AND_TAKEOFF)

        elif self.state == TacticalState.ARM_AND_TAKEOFF:
            # Takeoff to first waypoint z
            target_z = self.config.get('patrol_altitude', -12.0)
            self.publish_trajectory_setpoint(0.0, 0.0, target_z, 0.0)
            
            if abs(self.local_position.z - target_z) < 1.0:
                self.get_logger().info("Takeoff altitude reached.")
                self.transition_to(TacticalState.MOVE_TO_PHASE_LINE)

        elif self.state == TacticalState.MOVE_TO_PHASE_LINE:
            if self.current_wp_index < len(self.mission_waypoints):
                wp = self.mission_waypoints[self.current_wp_index]
                self.publish_trajectory_setpoint(wp.x, wp.y, wp.z, 0.0)
                
                dist = math.sqrt((self.local_position.x - wp.x)**2 + (self.local_position.y - wp.y)**2)
                if dist < 2.0:
                    self.get_logger().info(f"Reached {wp.label}")
                    if wp.hold_seconds > 0:
                        self.transition_to(TacticalState.HOLD_AT_OP)
                    else:
                        self.current_wp_index += 1
                        if self.current_wp_index >= len(self.mission_waypoints):
                            self.transition_to(TacticalState.RTL)
            else:
                self.transition_to(TacticalState.RTL)

        elif self.state == TacticalState.HOLD_AT_OP:
            wp = self.mission_waypoints[self.current_wp_index]
            self.publish_trajectory_setpoint(wp.x, wp.y, wp.z, 0.0) # Hover
            
            elapsed = time.time() - self.state_start_time
            if elapsed > wp.hold_seconds:
                self.get_logger().info(f"Hold complete at {wp.label}")
                self.current_wp_index += 1
                if self.current_wp_index >= len(self.mission_waypoints):
                    self.transition_to(TacticalState.RTL)
                else:
                    self.transition_to(TacticalState.MOVE_TO_PHASE_LINE)

        elif self.state == TacticalState.RTL:
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_RETURN_TO_LAUNCH)
            # RTL mode will take over
            pass

    def transition_to(self, new_state):
        self.get_logger().info(f"Transitioning from {self.state.name} to {new_state.name}")
        self.state = new_state
        self.state_start_time = time.time()

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
        self.get_logger().info("Arm command sent")

    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_control_mode_publisher.publish(msg)

    def publish_trajectory_setpoint(self, x, y, z, yaw):
        msg = TrajectorySetpoint()
        msg.position = [float(x), float(y), float(z)]
        msg.yaw = float(yaw)
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_setpoint_publisher.publish(msg)

    def publish_vehicle_command(self, command, param1=0.0, param2=0.0, param3=0.0):
        msg = VehicleCommand()
        msg.param1 = float(param1)
        msg.param2 = float(param2)
        msg.param3 = float(param3)
        msg.command = command
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.vehicle_command_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TMCNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
