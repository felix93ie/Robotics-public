import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        
        # Parameters
        self.declare_parameter('model_name', 'yolov10n.pt')
        self.declare_parameter('confidence_threshold', 0.25)
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('skip_frames', 1)  # Process every 2nd frame (50% reduction in skipping)
        self.declare_parameter('imgsz', 640)  # YOLO input size (smaller = faster)
        
        model_name = self.get_parameter('model_name').value
        self.conf_threshold = self.get_parameter('confidence_threshold').value
        image_topic = self.get_parameter('image_topic').value
        self.skip_frames = self.get_parameter('skip_frames').value
        self.imgsz = self.get_parameter('imgsz').value
        self.frame_count = 0
        
        # Load YOLO model
        self.get_logger().info(f"Loading YOLO model: {model_name}...")
        self.model = YOLO(model_name)
        self.get_logger().info("YOLO model loaded successfully.")
        
        # CvBridge
        self.bridge = CvBridge()
        
        # Publishers
        self.detections_publisher = self.create_publisher(
            Detection2DArray, 
            '/scout_bot/detections', 
            10
        )
        self.debug_image_publisher = self.create_publisher(
            Image, 
            '/scout_bot/debug_image', 
            10
        )
        
        # Subscriber
        self.image_subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )
        
        self.get_logger().info(f"YoloNode initialized. Subscribed to: {image_topic}")

    def image_callback(self, msg):
        # Skip frames to reduce compute load
        self.frame_count += 1
        if self.frame_count % (self.skip_frames + 1) != 0:
            return
            
        try:
            # Convert ROS Image to OpenCV BGR
            cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return
            
        # Run inference with smaller input size for speed
        results = self.model(cv_img, conf=self.conf_threshold, verbose=False, imgsz=self.imgsz)
        
        if len(results) == 0:
            return
            
        result = results[0]
        
        # Construct ROS 2 detection message
        detection_array = Detection2DArray()
        detection_array.header = msg.header
        
        # Draw on debug image if there are subscribers
        draw_debug = self.debug_image_publisher.get_subscription_count() > 0
        debug_img = cv_img.copy() if draw_debug else None
        
        class_counts = {}
        
        for box in result.boxes:
            # Bounding box coords
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Confidence & class ID
            conf = float(box.conf[0].cpu().item())
            cls_id = int(box.cls[0].cpu().item())
            cls_name = self.model.names[cls_id]
            
            # Tally counts for watermark
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
            
            # Create Detection2D
            det = Detection2D()
            det.header = msg.header
            
            # Box center & size
            det.bbox.center.position.x = float((x1 + x2) / 2.0)
            det.bbox.center.position.y = float((y1 + y2) / 2.0)
            det.bbox.size_x = float(x2 - x1)
            det.bbox.size_y = float(y2 - y1)
            
            # Hypothesis
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = cls_name
            hyp.hypothesis.score = conf
            det.results.append(hyp)
            
            detection_array.detections.append(det)
            
            # Draw on debug image
            if draw_debug:
                cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                label = f"{cls_name} {conf:.2f}"
                cv2.putText(debug_img, label, (x1, max(y1 - 10, 0)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            
        # Publish detections
        self.detections_publisher.publish(detection_array)
        
        # Publish debug image
        if draw_debug:
            # Draw Watermark HUD
            y_offset = 30
            cv2.putText(debug_img, "TARGETS IN FRAME:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            if not class_counts:
                cv2.putText(debug_img, "NONE", (20, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            else:
                for cls_name, count in class_counts.items():
                    y_offset += 25
                    text = f"- {count}x {cls_name.upper()}"
                    cv2.putText(debug_img, text, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    
            try:
                debug_msg = self.bridge.cv2_to_imgmsg(debug_img, encoding='bgr8')
                debug_msg.header = msg.header
                self.debug_image_publisher.publish(debug_msg)
            except Exception as e:
                self.get_logger().error(f"Failed to publish debug image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
