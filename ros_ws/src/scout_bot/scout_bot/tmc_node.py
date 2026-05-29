import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleStatus, VehicleLocalPosition
from vision_msgs.msg import Detection2DArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import math
import time
import yaml
from enum import Enum
from ament_index_python.packages import get_package_share_directory
import os
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==============================================================================
# Premium Dark Theme Web Dashboard HTML Asset
# ==============================================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AirScout Controller Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: rgba(16, 22, 37, 0.75);
            --border-color: rgba(0, 255, 135, 0.15);
            --border-glow: rgba(0, 255, 135, 0.3);
            --accent-cyan: #00ff87;
            --accent-blue: #02c77d;
            --accent-red: #ff2a5f;
            --accent-orange: #f39c12;
            --text-main: #e2e8f0;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 255, 135, 0.03) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(255, 42, 95, 0.03) 0%, transparent 40%);
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
        }

        h1 {
            font-size: 24px;
            font-weight: 900;
            letter-spacing: 2px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 600;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .pulse-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan);
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 15px var(--accent-cyan); }
            100% { transform: scale(0.9); opacity: 0.6; }
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 20px;
            flex-grow: 1;
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .main-panel {
            display: grid;
            grid-template-rows: auto 1fr;
            gap: 20px;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover {
            border-color: var(--border-glow);
            box-shadow: 0 8px 32px rgba(0, 242, 254, 0.08);
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--accent-blue);
            margin-bottom: 16px;
            border-left: 3px solid var(--accent-cyan);
            padding-left: 10px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }

        label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            background: rgba(8, 12, 20, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-main);
            font-family: 'Share Tech Mono', monospace;
            font-size: 16px;
            outline: none;
            transition: all 0.3s;
        }

        input[type="text"]:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }

        .mode-cards {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .mode-card {
            background: rgba(8, 12, 20, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .mode-card.selected {
            border-color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.05);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.1);
        }

        .mode-name {
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .mode-desc {
            font-size: 12px;
            color: var(--text-muted);
        }

        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-launch {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #05070c;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);
        }

        .btn-launch:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4);
        }

        .btn-abort {
            background: rgba(255, 42, 95, 0.1);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            margin-top: 10px;
        }

        .btn-abort:hover {
            background: var(--accent-red);
            color: #fff;
            box-shadow: 0 4px 15px rgba(255, 42, 95, 0.3);
        }

        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }

        .telemetry-item {
            background: rgba(8, 12, 20, 0.5);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .telemetry-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .telemetry-value {
            font-family: 'Share Tech Mono', monospace;
            font-size: 20px;
            font-weight: 700;
            color: var(--accent-cyan);
        }

        .state-active {
            color: var(--accent-orange);
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            50% { opacity: 0.5; }
        }

        .bottom-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .logs-container {
            font-family: 'Share Tech Mono', monospace;
            font-size: 13px;
            background: rgba(5, 8, 14, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            height: 250px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            white-space: pre-wrap;
        }

        .log-entry {
            line-height: 1.4;
        }

        .log-info { color: #5ce1e6; }
        .log-warn { color: var(--accent-orange); }
        .log-error { color: var(--accent-red); }

        .threats-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            height: 250px;
            overflow-y: auto;
        }

        .threat-item {
            background: rgba(255, 42, 95, 0.05);
            border: 1px solid rgba(255, 42, 95, 0.2);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from { transform: translateY(10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .threat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .threat-class {
            font-weight: 800;
            color: var(--accent-red);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .threat-time {
            font-size: 11px;
            color: var(--text-muted);
        }

        .threat-details {
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            color: var(--text-main);
        }

        .no-threats {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            color: var(--text-muted);
            font-size: 14px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <header>
        <h1>AIRSCOUT CONTROLLER</h1>
        <div class="status-indicator">
            <div class="pulse-dot"></div>
            <span>System Telemetry Link: Active</span>
        </div>
    </header>

    <div class="dashboard-grid">
        <!-- Sidebar Controls -->
        <div class="sidebar">
            <div class="card" style="flex-grow: 1; display: flex; flex-direction: column;">
                <div class="card-title">Mission Setup</div>
                <div style="flex-grow: 1;">
                    <div class="control-group">
                        <label>Target MGRS Coordinates</label>
                        <input type="text" id="mgrs-input" value="10SEG 88650 41222">
                    </div>

                    <div class="control-group">
                        <label>Mission Doctrine Mode</label>
                        <div class="mode-cards">
                            <div class="mode-card selected" onclick="selectMode('scan')" id="mode-scan">
                                <div class="mode-name">Investigate &amp; Scan</div>
                                <div class="mode-desc">Complete 360 optics scan. Reports intelligence post-scan.</div>
                            </div>
                            <div class="mode-card" onclick="selectMode('provoke')" id="mode-provoke">
                                <div class="mode-name">Recon by Fire</div>
                                <div class="mode-desc">Aggressive 30s figure-8 maneuvers to spook enemy forces.</div>
                            </div>
                            <div class="mode-card" onclick="selectMode('observe')" id="mode-observe">
                                <div class="mode-name">Observation Post</div>
                                <div class="mode-desc">Hover over target indefinitely to build reports.</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin-top: auto;">
                    <button class="btn btn-launch" onclick="launchMission()">Execute Objective</button>
                    <button class="btn btn-abort" onclick="abortMission()">Return Home/Recall</button>
                </div>
            </div>
        </div>

        <!-- Main Display -->
        <div class="main-panel">
            <!-- Telemetry Details -->
            <div class="card">
                <div class="card-title">Real-time Telemetry</div>
                <div class="telemetry-grid">
                    <div class="telemetry-item">
                        <div class="telemetry-label">Flight State</div>
                        <div class="telemetry-value state-active" id="tele-state">INIT</div>
                    </div>
                    <div class="telemetry-item">
                        <div class="telemetry-label">MGRS Position</div>
                        <div class="telemetry-value" id="tele-mgrs">10SEG 00000 00000</div>
                    </div>
                    <div class="telemetry-item">
                        <div class="telemetry-label">Altitude (Z)</div>
                        <div class="telemetry-value" id="tele-alt">0.0m</div>
                    </div>
                    <div class="telemetry-item">
                        <div class="telemetry-label">Speed</div>
                        <div class="telemetry-value" id="tele-speed">0.0 m/s</div>
                    </div>
                    <div class="telemetry-item">
                        <div class="telemetry-label">Active Mode</div>
                        <div class="telemetry-value" id="tele-mode">NONE</div>
                    </div>
                </div>
            </div>

            <!-- Bottom logs & threats -->
            <div class="bottom-grid">
                <div class="card" style="display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="card-title" style="margin-bottom: 0;">Contact Report</div>
                        <button class="btn btn-abort" style="padding: 6px 12px; font-size: 12px; border-radius: 6px; background: rgba(0, 255, 135, 0.1); border-color: rgba(0, 255, 135, 0.3); color: var(--accent-cyan);" onclick="clearReports()">Clear Reports</button>
                    </div>
                    <div class="threats-list" id="threats-container">
                        <div class="no-threats">No threats detected. Area clear.</div>
                    </div>
                </div>

                <div class="card" style="display: flex; flex-direction: column;">
                    <div class="card-title">Operations Log</div>
                    <div class="logs-container" id="logs-container"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedMode = 'scan';

        function selectMode(mode) {
            selectedMode = mode;
            document.getElementById('mode-scan').classList.remove('selected');
            document.getElementById('mode-provoke').classList.remove('selected');
            document.getElementById('mode-observe').classList.remove('selected');
            document.getElementById('mode-' + mode).classList.add('selected');
        }

        function clearReports() {
            fetch('/api/clear_reports', { method: 'POST' });
        }

        function launchMission() {
            const mgrsVal = document.getElementById('mgrs-input').value;
            fetch('/api/launch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mgrs: mgrsVal, mode: selectedMode })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) alert("Launch Error: " + data.message);
            })
            .catch(err => console.error("API Error:", err));
        }

        function abortMission() {
            fetch('/api/abort', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (!data.success) alert("Abort Error: " + data.message);
            })
            .catch(err => console.error("API Error:", err));
        }

        function updateTelemetry() {
            fetch('/api/status')
            .then(res => res.json())
            .then(data => {
                document.getElementById('tele-state').innerText = data.state;
                document.getElementById('tele-mgrs').innerText = data.mgrs;
                
                const altVal = -data.z;
                document.getElementById('tele-alt').innerText = altVal.toFixed(1) + "m";
                document.getElementById('tele-speed').innerText = data.speed.toFixed(2) + " m/s";
                document.getElementById('tele-mode').innerText = data.mode.toUpperCase();

                const teleState = document.getElementById('tele-state');
                if (data.state === 'WAITING_FOR_COMMAND' || data.state === 'STANDBY') {
                    teleState.className = 'telemetry-value';
                    teleState.style.color = '#00f2fe';
                } else if (data.state === 'PROVOKING') {
                    teleState.className = 'telemetry-value state-active';
                    teleState.style.color = '#ff2a5f';
                } else {
                    teleState.className = 'telemetry-value state-active';
                    teleState.style.color = '#f39c12';
                }

                const logsContainer = document.getElementById('logs-container');
                logsContainer.innerHTML = data.logs.map(log => {
                    let className = 'log-info';
                    if (log.includes('WARN:')) className = 'log-warn';
                    if (log.includes('ERROR:') || log.includes('🚨') || log.includes('📋')) className = 'log-error';
                    return `<div class="log-entry ${className}">${log}</div>`;
                }).join('');
                logsContainer.scrollTop = logsContainer.scrollHeight;

                const threatsContainer = document.getElementById('threats-container');
                if (data.threats.length === 0) {
                    threatsContainer.innerHTML = '<div class="no-threats">No threats detected. Area clear.</div>';
                } else {
                    threatsContainer.innerHTML = data.threats.map(threat => `
                        <div class="threat-item">
                            <div class="threat-header">
                                <span class="threat-class">⚠️ CONTACT: ${threat.class}</span>
                                <span class="threat-time">${threat.timestamp}</span>
                            </div>
                            <div class="threat-details">
                                Count: ${threat.count} | Loc: ${threat.mgrs} | Conf: ${threat.confidence}
                            </div>
                        </div>
                    `).join('');
                }
            })
            .catch(err => console.error("Telemetry update failed:", err));
        }

        setInterval(updateTelemetry, 500);
    </script>
</body>
</html>
"""
# ==============================================================================

class TacticalHTTPRequestHandler(BaseHTTPRequestHandler):
    node = None
    
    def log_message(self, format, *args):
        # Suppress logging to keep the ROS 2 terminal clean
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode('utf-8'))
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status_data = {
                'state': 'STANDBY' if self.node.state.name == 'WAITING_FOR_COMMAND' else self.node.state.name,
                'mode': self.node.mission_mode or "None",
                'x': round(self.node.local_position.x, 2),
                'y': round(self.node.local_position.y, 2),
                'z': round(self.node.local_position.z, 2),
                'speed': round(self.node.get_current_speed(), 2),
                'mgrs': self.node.get_current_mgrs(),
                'threats': self.node.threat_reports,
                'logs': self.node.console_logs[-20:]
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
        elif self.path == '/api/clear_reports':
            self.node.threat_reports = []
            response = {'success': True}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/launch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            
            mgrs_str = params.get('mgrs', '')
            mode = params.get('mode', '')
            
            try:
                x, y = self.node.parse_mgrs(mgrs_str)
                self.node.target_x = x
                self.node.target_y = y
                self.node.mission_mode = mode
                self.node.trigger_launch()
                
                response = {'success': True, 'message': 'Mission launched successfully.'}
                self.send_response(200)
            except Exception as e:
                response = {'success': False, 'message': str(e)}
                self.send_response(400)
                
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        elif self.path == '/api/abort':
            self.node.trigger_abort()
            response = {'success': True, 'message': 'Mission aborted. Returning home.'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/api/clear_reports':
            self.node.threat_reports = []
            response = {'success': True}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

class TacticalState(Enum):
    INIT = 0
    ARM_AND_TAKEOFF = 1
    WAITING_FOR_COMMAND = 2
    ENROUTE = 3
    SCANNING = 4
    OBSERVING = 5
    PROVOKING = 6
    RTL = 7
    LANDED = 8

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
        
        # YOLO Detection Subscriber
        self.detections_subscriber = self.create_subscription(
            Detection2DArray,
            '/scout_bot/detections',
            self.detections_callback,
            10
        )
        
        # Depth Camera Subscriber
        self.depth_subscriber = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depth_callback,
            10
        )
        
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz
        
        # CvBridge
        self.bridge = CvBridge()
        
        # State variables
        self.state = TacticalState.LANDED  # Wait on the ground until user dispatches a mission!
        self.vehicle_status = VehicleStatus()
        self.local_position = VehicleLocalPosition()
        self.status_received = False
        self.position_received = False
        self.state_start_time = 0.0
        
        # Target coordinates & mission mode variables
        self.mission_mode = None
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = -25.0 # Safe flight altitude (25m clears 15m trees on 18m hills)
        self.home_z = -25.0
        
        # Sensor depth readings
        self.d_left = 100.0
        self.d_center = 100.0
        self.d_right = 100.0
        self.depth_received_count = 0
        self.prev_commanded_z = self.home_z  # For Z rate limiting
        self._last_stale_check_time = 0.0
        self._last_stale_rx = 0
        
        # Log and intelligence report structures
        self.console_logs = []
        self.threat_reports = []  # Permanent database shown on dashboard
        self.scan_threats = []    # Temporary list for current active scan
        
        # Start Web Server Thread
        TacticalHTTPRequestHandler.node = self
        self.server = HTTPServer(('0.0.0.0', 8080), TacticalHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.log_info("TMC Node initialized. Dashboard server hosted at http://localhost:8080")

    def log_info(self, msg):
        self.get_logger().info(msg)
        self.console_logs.append(f"[{time.strftime('%H:%M:%S')}] INFO: {msg}")

    def log_warn(self, msg):
        self.get_logger().warn(msg)
        self.console_logs.append(f"[{time.strftime('%H:%M:%S')}] WARN: {msg}")

    def parse_mgrs(self, mgrs_str):
        s = mgrs_str.replace(" ", "").upper()
        if not s.startswith("10SEG"):
            raise ValueError("Invalid MGRS format. Must start with '10SEG'.")
            
        coords_part = s[5:]
        if len(coords_part) == 10 and coords_part.isdigit():
            easting_str = coords_part[:5]
            northing_str = coords_part[5:]
        elif len(coords_part) == 8 and coords_part.isdigit():
            easting_str = coords_part[:4] + "0"
            northing_str = coords_part[4:] + "0"
        else:
            raise ValueError("MGRS coordinates must contain 8 or 10 digits after '10SEG'.")
            
        e_target = float(easting_str)
        n_target = float(northing_str)
        
        # Map to localized simulation coordinates
        origin_e = 88523.5
        origin_n = 41042.8
        
        # Gazebo ENU X is East (maps to PX4 Y/East), Y is North (maps to PX4 X/North)
        x_px4 = n_target - origin_n  # North offset
        y_px4 = e_target - origin_e  # East offset
        
        return x_px4, y_px4

    def get_current_mgrs(self):
        x = self.local_position.x  # PX4 X is North
        y = self.local_position.y  # PX4 Y is East
        e = 88523.5 + y  # Easting
        n = 41042.8 + x  # Northing
        e_str = f"{int(max(0.0, min(99999.0, e))):05d}"
        n_str = f"{int(max(0.0, min(99999.0, n))):05d}"
        return f"10SEG {e_str} {n_str}"

    def get_terrain_height(self, x, y):
        # x is PX4 X (North), y is PX4 Y (East)
        # Hill 1 parameters from world SDF (h1_x is East, h1_y is North)
        h1_x, h1_y, h1_z, h1_r = 126.782, 179.08, -35.45, 53.45
        # Hill 2 parameters from world SDF (h2_x is East, h2_y is North)
        h2_x, h2_y, h2_z, h2_r = 419.248, -34.83, -18.45, 40.45
        
        # Compare PX4 Y (East) to SDF X (East), and PX4 X (North) to SDF Y (North)
        d1 = math.sqrt((y - h1_x)**2 + (x - h1_y)**2)
        d2 = math.sqrt((y - h2_x)**2 + (x - h2_y)**2)
        
        h_terrain = 0.0
        if d1 < h1_r:
            # Reconstruct visual surface height (Z relative to sea level)
            h_terrain = max(h_terrain, h1_z + math.sqrt(h1_r**2 - d1**2))
        if d2 < h2_r:
            h_terrain = max(h_terrain, h2_z + math.sqrt(h2_r**2 - d2**2))
            
        return h_terrain

    def get_current_speed(self):
        vx = self.local_position.vx if hasattr(self.local_position, 'vx') and not math.isnan(self.local_position.vx) else 0.0
        vy = self.local_position.vy if hasattr(self.local_position, 'vy') and not math.isnan(self.local_position.vy) else 0.0
        vz = self.local_position.vz if hasattr(self.local_position, 'vz') and not math.isnan(self.local_position.vz) else 0.0
        return math.sqrt(vx**2 + vy**2 + vz**2)

    def trigger_launch(self):
        self.log_warn(f"🚀 LAUNCH COMMAND: {self.mission_mode.upper()} to Target X={self.target_x:.2f}, Y={self.target_y:.2f} ({self.get_current_mgrs()})")
        
        # If we are interrupting an active intelligence-gathering mission, compile what we saw first!
        if self.state in [TacticalState.SCANNING, TacticalState.OBSERVING] or self.scan_threats:
            self.log_warn("Interrupting active intelligence gathering. Compiling preliminary report...")
            self.compile_and_publish_report()
            
        if self.state in [TacticalState.INIT, TacticalState.LANDED]:
            self.has_pending_command = True
            self.transition_to(TacticalState.INIT)
        else:
            self.transition_to(TacticalState.ENROUTE)

    def compile_and_publish_report(self):
        if self.scan_threats:
            self.log_warn(f"📋 CONSOLIDATED INTEL REPORT: Spotted {len(self.scan_threats)} distinct threat clusters!")
            for threat in self.scan_threats:
                # Avoid duplicates in the global report
                dup = False
                for existing in self.threat_reports:
                    if existing['mgrs'] == threat['mgrs'] and existing['class'] == threat['class']:
                        # Update max count if we saw more
                        if threat['count'] > existing['count']:
                            existing['count'] = threat['count']
                            existing['timestamp'] = threat['timestamp']
                        dup = True
                        break
                if not dup:
                    self.threat_reports.append(threat)
                self.log_warn(f"   - Threat: {threat['class']} | Count: {threat['count']} | Location: {threat['mgrs']}")
        else:
            self.log_info("📋 CONSOLIDATED INTEL REPORT: Target coordinate area is clear of threats.")
            
    def trigger_abort(self):
        self.log_warn("⚠️ RECALL INITIATED. Ordering immediate Return Home.")
        if self.state in [TacticalState.SCANNING, TacticalState.OBSERVING] or self.scan_threats:
            self.compile_and_publish_report()
        self.transition_to(TacticalState.RTL)

    def calculate_avoidance_step(self, target_x, target_y, target_z, align_yaw=True):
        pos_x = self.local_position.x
        pos_y = self.local_position.y
        pos_z = self.local_position.z
        
        dx_g = target_x - pos_x
        dy_g = target_y - pos_y
        dist_g = math.sqrt(dx_g**2 + dy_g**2)
        
        if dist_g < 0.2:
            return target_x, target_y, target_z
            
        # APF parameters
        k_att = 1.5  # Increased attractive pull to reduce wandering
        k_rep_center = 1500.0  # Slightly softened to reduce bounce
        k_rep_side = 800.0
        eta = 12.0  # Safety distance (meters)
        
        # Dynamic Speed Scaling (Shift to moving really fast when skyline is clear)
        min_depth = min(self.d_left, self.d_center, self.d_right)
        if min_depth > 15.0:
            max_vel = 12.0
        elif min_depth > 10.0:
            max_vel = 4.0 + 8.0 * ((min_depth - 10.0) / 5.0)  # Linear ramp down to 4.0
        else:
            max_vel = 4.0
            
        dt = 0.1
        bias_mag = 2.0  # Reduced bias to smooth out lateral strafing
        
        f_att_x = k_att * dx_g / dist_g
        f_att_y = k_att * dy_g / dist_g
        
        f_rep_body_x = 0.0
        f_rep_body_y = 0.0
        
        d_left_val = max(self.d_left, 1.0)
        d_center_val = max(self.d_center, 1.0)
        d_right_val = max(self.d_right, 1.0)
        
        if self.d_center < eta:
            f_rep_body_x -= k_rep_center * (1.0 / d_center_val - 1.0 / eta) * (1.0 / (d_center_val**2))
            if self.d_left >= self.d_right:
                f_rep_body_y -= bias_mag
            else:
                f_rep_body_y += bias_mag
                
        if self.d_left < eta:
            f_rep_body_y += k_rep_side * (1.0 / d_left_val - 1.0 / eta) * (1.0 / (d_left_val**2))
            
        if self.d_right < eta:
            f_rep_body_y -= k_rep_side * (1.0 / d_right_val - 1.0 / eta) * (1.0 / (d_right_val**2))
            
        psi = self.local_position.heading if hasattr(self.local_position, 'heading') and not math.isnan(self.local_position.heading) else 0.0
        
        f_rep_x = f_rep_body_x * math.cos(psi) - f_rep_body_y * math.sin(psi)
        f_rep_y = f_rep_body_x * math.sin(psi) + f_rep_body_y * math.cos(psi)
        
        f_net_x = f_att_x + f_rep_x
        f_net_y = f_att_y + f_rep_y
        f_net_mag = math.sqrt(f_net_x**2 + f_net_y**2)
        
        if f_net_mag > 0.01:
            dir_x = f_net_x / f_net_mag
            dir_y = f_net_y / f_net_mag
        else:
            dir_x, dir_y = 0.0, 0.0
            
        # Exponential Moving Average (EMA) filter to smooth the direction vector and reduce oscillation
        if not hasattr(self, 'last_dir_x'):
            self.last_dir_x = dir_x
            self.last_dir_y = dir_y
        
        alpha = 0.8  # Light smoothing: 80% new, 20% old (prevents phase-lag overshoot)
        self.last_dir_x = alpha * dir_x + (1.0 - alpha) * self.last_dir_x
        self.last_dir_y = alpha * dir_y + (1.0 - alpha) * self.last_dir_y
        
        # Re-normalize smoothed vector to maintain speed
        smooth_mag = math.sqrt(self.last_dir_x**2 + self.last_dir_y**2)
        if smooth_mag > 0.01:
            self.last_dir_x /= smooth_mag
            self.last_dir_y /= smooth_mag
            
        # Dynamically scale down lookahead when close to obstacles to prevent overshooting
        lookahead = min(max_vel, dist_g)
        if self.d_center < eta:
            # Scale lookahead proportionally with center depth (minimum 1.5m to maintain command flow)
            lookahead = min(lookahead, max(1.5, 4.0 * (d_center_val / eta)))
            
        # If align_yaw is enabled, scale down lookahead based on yaw alignment error to prevent blind strafing
        if align_yaw:
            target_yaw = math.atan2(dir_y, dir_x)
            yaw_err = abs(target_yaw - psi)
            yaw_err = (yaw_err + math.pi) % (2.0 * math.pi) - math.pi
            yaw_err = abs(yaw_err)
            
            # Reduce step size if yaw error is large (e.g. up to 90% reduction if facing completely wrong way)
            yaw_scale = max(0.3, 1.0 - 0.7 * (yaw_err / (math.pi / 2.0)))
            lookahead *= yaw_scale
            
        next_x = pos_x + self.last_dir_x * lookahead
        next_y = pos_y + self.last_dir_y * lookahead
        
        # Calculate current speed from PX4 local position telemetry
        vx = self.local_position.vx if hasattr(self.local_position, 'vx') and not math.isnan(self.local_position.vx) else 0.0
        vy = self.local_position.vy if hasattr(self.local_position, 'vy') and not math.isnan(self.local_position.vy) else 0.0
        vz = self.local_position.vz if hasattr(self.local_position, 'vz') and not math.isnan(self.local_position.vz) else 0.0
        spd_3d = math.sqrt(vx**2 + vy**2 + vz**2)
        
        # Throttled logging for debugging
        if not hasattr(self, 'log_counter'):
            self.log_counter = 0
        self.log_counter += 1
        if self.log_counter % 10 == 0:
            self.get_logger().info(
                f"Speed: {spd_3d:.2f} m/s | Depth (rx: {self.depth_received_count}) - L: {self.d_left:.2f}m, C: {self.d_center:.2f}m, R: {self.d_right:.2f}m | "
                f"Rep Force Body - X: {f_rep_body_x:.2f}, Y: {f_rep_body_y:.2f}"
            )
            # Warn if depth data is stale (bridge not streaming)
            now = time.time()
            if now - self._last_stale_check_time > 3.0:
                if self.depth_received_count == self._last_stale_rx and self.depth_received_count > 0:
                    self.get_logger().warn(
                        f"⚠️ DEPTH STALE: rx={self.depth_received_count} unchanged for 3s. "
                        f"Check bridge: is /camera/depth/image_raw publishing?"
                    )
                self._last_stale_rx = self.depth_received_count
                self._last_stale_check_time = now
            
        # Add Z repulsive force to climb dynamically over obstacles
        f_rep_z = 0.0
        min_d = min(d_left_val, d_center_val, d_right_val)
        if min_d < eta:
            k_rep_z = 2500.0
            f_rep_z = - k_rep_z * (1.0 / min_d - 1.0 / eta) * (1.0 / (min_d**2))
            # Cap the Z avoidance climb to 15m above target_z (Z is negative upwards)
            f_rep_z = max(f_rep_z, -15.0)
            
        avoid_z = target_z + f_rep_z
        
        # Rate-limit Z changes to prevent wild altitude oscillation (max 3 m/s vertical)
        max_z_step = 0.3  # 0.3m per 0.1s tick = 3 m/s vertical rate
        if avoid_z < self.prev_commanded_z - max_z_step:
            avoid_z = self.prev_commanded_z - max_z_step
        elif avoid_z > self.prev_commanded_z + max_z_step:
            avoid_z = self.prev_commanded_z + max_z_step
        self.prev_commanded_z = avoid_z
        
        dist_step = math.sqrt((next_x - pos_x)**2 + (next_y - pos_y)**2)
        if dist_step > dist_g:
            return target_x, target_y, avoid_z
            
        return next_x, next_y, avoid_z

    def vehicle_status_callback(self, msg):
        self.vehicle_status = msg
        self.status_received = True

    def vehicle_local_position_callback(self, msg):
        self.local_position = msg
        self.position_received = True

    def depth_callback(self, msg):
        self.depth_received_count += 1
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            
            if cv_img.dtype == np.uint16:
                depth_in_meters = cv_img.astype(np.float32) / 1000.0
            else:
                depth_in_meters = cv_img.astype(np.float32)
                
            depth_in_meters = np.nan_to_num(depth_in_meters, nan=100.0, posinf=100.0, neginf=100.0)
            
            h, w = depth_in_meters.shape
            mid_row = h // 2
            row_span = min(20, mid_row)
            start_row = mid_row - row_span
            end_row = mid_row + row_span
            
            band = depth_in_meters[start_row:end_row, :]
            
            col_width = w // 3
            left_sector = band[:, :col_width]
            center_sector = band[:, col_width:2*col_width]
            right_sector = band[:, 2*col_width:]
            
            left_valid = left_sector[left_sector >= 0.1]
            center_valid = center_sector[center_sector >= 0.1]
            right_valid = right_sector[right_sector >= 0.1]
            
            self.d_left = float(np.min(left_valid)) if left_valid.size > 0 else 100.0
            self.d_center = float(np.min(center_valid)) if center_valid.size > 0 else 100.0
            self.d_right = float(np.min(right_valid)) if right_valid.size > 0 else 100.0
            
        except Exception as e:
            self.get_logger().error(f"Failed to process depth image: {e}")
            
    def estimate_target_location(self, bbox_y_center, image_height=480.0):
        """
        Calculates the estimated ground coordinate (x,y) of a detected object
        using the drone's altitude, heading, and the camera's fixed downward pitch.
        """
        # Drone altitude Above Ground Level (AGL)
        terrain_z = self.get_terrain_height(self.local_position.x, self.local_position.y)
        # local_position.z is negative (NED/ENU flipped), so use absolute altitude
        agl = abs(self.local_position.z - terrain_z)
        
        # Camera fixed pitch (35 degrees down)
        camera_pitch = 0.61  # radians
        
        # Normalize bounding box Y center from -1 (top) to +1 (bottom)
        norm_y = (bbox_y_center - (image_height / 2.0)) / (image_height / 2.0)
        
        # Vertical Field of View of camera is approx 0.95 rad (54 degrees)
        v_fov = 0.95 
        
        # Angle of the object below the camera's center axis
        alpha = norm_y * (v_fov / 2.0)
        
        # Total angle below the horizon
        theta_down = camera_pitch + alpha
        
        # If object is above horizon, we can't project it to the ground
        if theta_down <= 0.05:
            theta_down = 0.05
            
        # Ground distance from drone to object
        ground_dist = agl * math.tan(math.pi/2.0 - theta_down)  # identical to agl / tan(theta_down)
        
        # Drone compass heading
        heading = self.local_position.heading if hasattr(self.local_position, 'heading') and not math.isnan(self.local_position.heading) else 0.0
        
        # Object global coordinate
        obj_x = self.local_position.x + ground_dist * math.cos(heading)
        obj_y = self.local_position.y + ground_dist * math.sin(heading)
        
        return obj_x, obj_y

    def detections_callback(self, msg):
        # Collect threats during ENROUTE approach and SCANNING rotation states
        if self.state in [TacticalState.ENROUTE, TacticalState.SCANNING, TacticalState.OBSERVING]:
            frame_counts = {}
            
            for det in msg.detections:
                for res in det.results:
                    cls_name = res.hypothesis.class_id
                    conf = res.hypothesis.score
                    
                    threat_classes = ['car', 'truck', 'person', 'bus', 'motorcycle', 'airplane']
                    if cls_name in threat_classes and conf > 0.35:
                        box_cy = det.bbox.center.position.y
                        
                        # Project pixel to ground coordinate
                        obj_x, obj_y = self.estimate_target_location(box_cy)
                        
                        # Filter duplicate detections in current scan using a tight 2.5m radius
                        matched_idx = -1
                        for i, t in enumerate(self.scan_threats):
                            dist = math.sqrt((t['x'] - obj_x)**2 + (t['y'] - obj_y)**2)
                            if t['class'] == cls_name.upper() and dist < 2.5:
                                matched_idx = i
                                break
                                
                        if matched_idx == -1:
                            # New unique cluster found
                            e = 88523.5 + obj_y  # Easting
                            n = 41042.8 + obj_x  # Northing
                            e_str = f"{int(max(0.0, min(99999.0, e))):05d}"
                            n_str = f"{int(max(0.0, min(99999.0, n))):05d}"
                            obj_mgrs = f"10SEG {e_str} {n_str}"
                            
                            threat = {
                                'timestamp': time.strftime("%H:%M:%S"),
                                'class': cls_name.upper(),
                                'confidence': f"{conf*100:.1f}%",
                                'x': obj_x,
                                'y': obj_y,
                                'mgrs': obj_mgrs,
                                'count': 1
                            }
                            self.scan_threats.append(threat)
                            matched_idx = len(self.scan_threats) - 1
                            self.log_warn(f"Target cluster identified on ground: {cls_name.upper()} at {obj_mgrs}")
                        
                        # Increment frame tally for this matched cluster
                        frame_counts[matched_idx] = frame_counts.get(matched_idx, 0) + 1
            
            # Apply High-Water Mark: update max count if we saw more in this single frame
            for idx, count in frame_counts.items():
                if count > self.scan_threats[idx]['count']:
                    self.scan_threats[idx]['count'] = count
                    self.log_info(f"Cluster count updated! Now seeing {count} {self.scan_threats[idx]['class']}s at {self.scan_threats[idx]['mgrs']}")

    def timer_callback(self):
        if not self.status_received or not self.position_received:
            return
            
        self.publish_offboard_control_mode()
        
        if self.state == TacticalState.INIT:
            if self.vehicle_status.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
                self.transition_to(TacticalState.ARM_AND_TAKEOFF)
            else:
                self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
                self.arm()
                self.transition_to(TacticalState.ARM_AND_TAKEOFF)

        elif self.state == TacticalState.ARM_AND_TAKEOFF:
            self.publish_trajectory_setpoint(0.0, 0.0, self.home_z, 0.0)
            if abs(self.local_position.z - self.home_z) < 1.0:
                self.log_info("Takeoff altitude reached.")
                if getattr(self, 'has_pending_command', False):
                    self.transition_to(TacticalState.ENROUTE)
                    self.has_pending_command = False
                else:
                    self.transition_to(TacticalState.WAITING_FOR_COMMAND)

        elif self.state == TacticalState.WAITING_FOR_COMMAND:
            self.publish_trajectory_setpoint(0.0, 0.0, self.home_z, 0.0)

        elif self.state == TacticalState.ENROUTE:
            # Dynamic terrain climbing based on current coordinates
            curr_terrain = self.get_terrain_height(self.local_position.x, self.local_position.y)
            # Cruise altitude: 20m AGL to clear trees and prevent the pitched-down depth camera from seeing the ground
            current_target_z = -20.0 - curr_terrain
            
            # Enable align_yaw=True so the depth camera points towards the velocity vector!
            avoid_x, avoid_y, avoid_z = self.calculate_avoidance_step(self.target_x, self.target_y, current_target_z, align_yaw=True)
            
            # Align yaw with the actual direction of motion
            vx = avoid_x - self.local_position.x
            vy = avoid_y - self.local_position.y
            dist_step = math.sqrt(vx**2 + vy**2)
            
            if dist_step > 0.1:
                target_yaw = math.atan2(vy, vx)
            else:
                dx_t = self.target_x - self.local_position.x
                dy_t = self.target_y - self.local_position.y
                dist_g = math.sqrt(dx_t**2 + dy_t**2)
                target_yaw = math.atan2(dy_t, dx_t) if dist_g > 0.5 else 0.0
            
            # Smooth the yaw physically so the drone doesn't violently snap its heading back and forth
            current_yaw = self.local_position.heading if hasattr(self.local_position, 'heading') and not math.isnan(self.local_position.heading) else 0.0
            
            # Shortest path yaw interpolation
            yaw_diff = (target_yaw - current_yaw + math.pi) % (2.0 * math.pi) - math.pi
            
            # Dampen yaw rotation: max 2.5 radians (~140 degrees) per second so the nose can track the velocity vector!
            max_yaw_rate = 2.5 * 0.1 # 0.1s loop rate
            if abs(yaw_diff) > max_yaw_rate:
                yaw_diff = math.copysign(max_yaw_rate, yaw_diff)
                
            smoothed_yaw = current_yaw + yaw_diff
            smoothed_yaw = (smoothed_yaw + math.pi) % (2.0 * math.pi) - math.pi
            
            self.publish_trajectory_setpoint(avoid_x, avoid_y, avoid_z, smoothed_yaw)
            
            dx_t = self.target_x - self.local_position.x
            dy_t = self.target_y - self.local_position.y
            dist_g = math.sqrt(dx_t**2 + dy_t**2)
            if dist_g < 3.0:
                self.log_info(f"Target location reached. Mode: {self.mission_mode.upper()}. Initiating execution phase.")
                if self.mission_mode == "scan":
                    self.transition_to(TacticalState.SCANNING)
                elif self.mission_mode == "observe":
                    self.transition_to(TacticalState.OBSERVING)
                elif self.mission_mode == "provoke":
                    self.transition_to(TacticalState.PROVOKING)
                else:
                    self.transition_to(TacticalState.SCANNING)

        elif self.state == TacticalState.SCANNING:
            elapsed = time.time() - self.state_start_time
            scan_duration = 60.0
            
            # Altitude set to 10m AGL for closer inspection and slower flight
            target_z = -10.0 - self.get_terrain_height(self.target_x, self.target_y)
            
            if elapsed < scan_duration:
                # Calculate the mathematically perfect orbit radius to keep the target dead center in the camera frame
                # Camera is pitched down 35 degrees. tan(35) = altitude / Radius
                camera_pitch_rad = math.radians(35.0)
                R = 10.0 / math.tan(camera_pitch_rad)  # approx 14.28m
                
                # Calculate a circular orbit pattern
                theta = (elapsed / scan_duration) * 2.0 * math.pi
                
                orbit_x = self.target_x + R * math.cos(theta)
                orbit_y = self.target_y + R * math.sin(theta)
                
                # Apply obstacle avoidance on the orbit path
                avoid_x, avoid_y, avoid_z = self.calculate_avoidance_step(orbit_x, orbit_y, target_z, align_yaw=False)
                
                # Keep the nose (and camera) pointed directly at the target center
                dx = self.target_x - self.local_position.x
                dy = self.target_y - self.local_position.y
                yaw_target = math.atan2(dy, dx)
                
                self.publish_trajectory_setpoint(avoid_x, avoid_y, avoid_z, yaw_target)
            else:
                # 360 scan complete: compile and publish the report
                self.compile_and_publish_report()
                
                # Displace and return home
                self.transition_to(TacticalState.RTL)

        elif self.state == TacticalState.OBSERVING:
            # Stand off 21 meters South of the target so the 35-deg down-pitched camera sees it
            target_z = -15.0 - self.get_terrain_height(self.target_x, self.target_y)
            standoff_x = self.target_x
            standoff_y = self.target_y - 21.0
            avoid_x, avoid_y, avoid_z = self.calculate_avoidance_step(standoff_x, standoff_y, target_z, align_yaw=False)
            
            # Point nose (camera) North directly towards the target
            dx = self.target_x - self.local_position.x
            dy = self.target_y - self.local_position.y
            yaw_target = math.atan2(dy, dx)
            
            self.publish_trajectory_setpoint(avoid_x, avoid_y, avoid_z, yaw_target)

        elif self.state == TacticalState.PROVOKING:
            elapsed = time.time() - self.state_start_time
            duration = 30.0  # Provocation maneuver for 30s
            
            if elapsed < duration:
                # Aggressive figure-8 (lemniscate) target crossing trajectory
                omega = 2.0 * math.pi / 6.0  # Horizontal period 6s
                denom = 1.0 + math.sin(omega * elapsed)**2
                ox = 20.0 * math.cos(omega * elapsed) / denom
                oy = 20.0 * math.sin(omega * elapsed) * math.cos(omega * elapsed) / denom
                
                target_pose_x = self.target_x + ox
                target_pose_y = self.target_y + oy
                
                # Dynamic terrain height at target swoop coordinate
                terrain_at_swoop = self.get_terrain_height(target_pose_x, target_pose_y)
                
                # Altitude oscillation (8m to 18m clearance above local terrain)
                omega_v = 2.0 * math.pi / 3.0  # Vertical period 3s
                clearance = 13.0 + 5.0 * math.sin(omega_v * elapsed)
                target_pose_z = self.home_z - terrain_at_swoop - (clearance - 12.0)
                
                avoid_x, avoid_y, avoid_z = self.calculate_avoidance_step(target_pose_x, target_pose_y, target_pose_z)
                
                # Align yaw with direction of travel to prevent blind crashes
                vx = avoid_x - self.local_position.x
                vy = avoid_y - self.local_position.y
                dist_step = math.sqrt(vx**2 + vy**2)
                yaw_target = math.atan2(vy, vx) if dist_step > 0.1 else 0.0
                
                self.publish_trajectory_setpoint(avoid_x, avoid_y, avoid_z, yaw_target)
            else:
                self.log_info("Recon by Fire decoy sequence complete. Displacing and returning home.")
                self.transition_to(TacticalState.RTL)

        elif self.state == TacticalState.RTL:
            # Dynamic terrain height for safe return flight
            curr_terrain = self.get_terrain_height(self.local_position.x, self.local_position.y)
            current_target_z = self.home_z - curr_terrain
            
            avoid_x, avoid_y, avoid_z = self.calculate_avoidance_step(0.0, 0.0, current_target_z)
            
            # Align yaw with direction of travel
            vx = avoid_x - self.local_position.x
            vy = avoid_y - self.local_position.y
            dist_step = math.sqrt(vx**2 + vy**2)
            
            if dist_step > 0.1:
                target_yaw = math.atan2(vy, vx)
            else:
                dx = 0.0 - self.local_position.x
                dy = 0.0 - self.local_position.y
                dist_home = math.sqrt(dx**2 + dy**2)
                target_yaw = math.atan2(dy, dx) if dist_home > 0.5 else 0.0
            
            self.publish_trajectory_setpoint(avoid_x, avoid_y, avoid_z, target_yaw)
            
            dx_h = 0.0 - self.local_position.x
            dy_h = 0.0 - self.local_position.y
            dist_home = math.sqrt(dx_h**2 + dy_h**2)
            if dist_home < 2.0:
                self.log_info("Home base reached. Initiating automatic landing sequence.")
                self.transition_to(TacticalState.LANDED)

        elif self.state == TacticalState.LANDED:
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)

    def transition_to(self, new_state):
        self.log_info(f"Transitioning from {self.state.name} to {new_state.name}")
        self.state = new_state
        self.state_start_time = time.time()
        if new_state == TacticalState.ENROUTE:
            self.scan_threats = []

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
        self.log_info("Arm command sent")

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

    def destroy_node(self):
        self.server.shutdown()
        self.server.server_close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = TMCNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass

if __name__ == '__main__':
    main()
