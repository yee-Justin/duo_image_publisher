import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from message_filters import Subscriber, ApproximateTimeSynchronizer
from cv_bridge import CvBridge
import cv2
import os

class StereoSyncNode(Node):
    def __init__(self):
        super().__init__('stereo_sync_node')
        self.bridge = CvBridge()

        # Create directories to save stereo pairs
        # Change these directories to whatever you prefer
        self.left_dir = '/home/justin/stereo_pairs/left'
        self.right_dir = '/home/justin/stereo_pairs/right'
        os.makedirs(self.left_dir, exist_ok=True)
        os.makedirs(self.right_dir, exist_ok=True)

        # Subscribe to both image topics
        self.left_sub = Subscriber(self, Image, '/camera2/image_raw')
        self.right_sub = Subscriber(self, Image, '/camera1/image_raw')

        # ApproximateTimeSynchronizer to sync frames
        self.ts = ApproximateTimeSynchronizer(
            [self.left_sub, self.right_sub],
            queue_size=10,
            slop=0.05  # max time difference in seconds
        )
        self.ts.registerCallback(self.stereo_callback)

        self.get_logger().info('📡 StereoSyncNode initialized and waiting for images...')

    def stereo_callback(self, left_msg, right_msg):
        try:
            # Convert ROS Image messages to OpenCV images
            left_image = self.bridge.imgmsg_to_cv2(left_msg, desired_encoding='bgr8')
            right_image = self.bridge.imgmsg_to_cv2(right_msg, desired_encoding='bgr8')

            # Use timestamp from left image for both files
            timestamp = left_msg.header.stamp.sec * 1_000_000_000 + left_msg.header.stamp.nanosec

            # Create filenames
            left_filename = os.path.join(self.left_dir, f'{timestamp}.jpg')
            right_filename = os.path.join(self.right_dir, f'{timestamp}.jpg')

            # Save images
            cv2.imwrite(left_filename, left_image)
            cv2.imwrite(right_filename, right_image)

            self.get_logger().info(f'💾 Saved stereo pair at timestamp {timestamp}')

        except Exception as e:
            self.get_logger().error(f'Error in stereo_callback: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = StereoSyncNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
