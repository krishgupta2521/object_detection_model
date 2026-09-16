import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImageSubscriber(Node):

    def __init__(self):
        super().__init__("image_subscriber")

        self.subscription = self.create_subscription(
            Image,
            "/camera/image_raw",
            self.image_callback,
            10
        )

        self.bridge = CvBridge()
        self.received_count = 0

        self.get_logger().info("Image Subscriber started")
        self.get_logger().info("Subscribed to /camera/image_raw")

    def image_callback(self, msg):

        # Convert ROS 2 Image message to OpenCV image
        image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding="bgr8"
        )

        self.received_count += 1

        # Get image dimensions using OpenCV
        height, width = image.shape[:2]

        # Calculate image center
        center_x = width // 2
        center_y = height // 2

        # Draw image center using OpenCV
        cv2.drawMarker(
            image,
            (center_x, center_y),
            (255, 0, 0),
            markerType=cv2.MARKER_CROSS,
            markerSize=30,
            thickness=2
        )

        # Add text
        cv2.putText(
            image,
            f"ROS 2 + OpenCV | Center: ({center_x}, {center_y})",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Display using OpenCV
        cv2.imshow(
            "ROS 2 + OpenCV Image Subscriber",
            image
        )

        cv2.waitKey(1)

        if self.received_count == 1:
            self.get_logger().info(
                f"Received image: {width}x{height}"
            )
            self.get_logger().info(
                f"OpenCV image center: ({center_x}, {center_y})"
            )


def main(args=None):

    rclpy.init(args=args)

    node = ImageSubscriber()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
