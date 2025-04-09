import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        # Declare parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('camera_id', '/dev/video0'),
                ('image_topic', 'image_raw')
            ]
        )

        # Get parameters
        camera_id_param = self.get_parameter('camera_id').get_parameter_value()
        if camera_id_param.type == 4:  # STRING
            self.camera_id = camera_id_param.string_value
        else:  # fallback to int index
            self.camera_id = camera_id_param.integer_value

        self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value

        # Open camera using V4L2 backend
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_V4L2)

        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Set MJPEG format
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        # Set up publisher and timer
        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(Image, self.image_topic, 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Confirm camera open
        if not self.cap.isOpened():
            self.get_logger().error(f'❌ Failed to open camera: {self.camera_id}')
        else:
            self.get_logger().info(f'✅ Camera opened: {self.camera_id}, publishing to: {self.image_topic}')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn(f'⚠️ Failed to read frame from camera {self.camera_id}')
            return

        # No need to convert from YUYV since MJPEG gives us BGR directly
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'camera_{str(self.camera_id).replace("/dev/", "")}_frame'
        self.publisher_.publish(msg)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        self.get_logger().info('🛑 Camera stream closed.')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
