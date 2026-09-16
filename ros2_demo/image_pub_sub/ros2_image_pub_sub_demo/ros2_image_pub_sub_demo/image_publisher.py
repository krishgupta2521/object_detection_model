import os

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImagePublisher(Node):

    def __init__(self):
        super().__init__("image_publisher")

        self.publisher = self.create_publisher(
            Image,
            "/camera/image_raw",
            10
        )

        self.bridge = CvBridge()

        image_path = os.path.join(
            os.path.dirname(__file__),
            "fish8.jpg"
        )

        self.image = cv2.imread(image_path)

        if self.image is None:
            self.get_logger().error(
                f"Could not read image: {image_path}"
            )
            raise RuntimeError("Image could not be loaded")

        self.timer = self.create_timer(
            1.0,
            self.publish_image
        )

        self.get_logger().info(
            "Image Publisher started"
        )

        self.get_logger().info(
            "Publishing fish8.jpg on /camera/image_raw"
        )

    def publish_image(self):

        msg = self.bridge.cv2_to_imgmsg(
            self.image,
            encoding="bgr8"
        )

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_link"

        self.publisher.publish(msg)

        self.get_logger().info(
            "Published image frame"
        )


def main(args=None):

    rclpy.init(args=args)

    node = ImagePublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
