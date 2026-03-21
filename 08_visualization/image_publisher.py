#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        
        self.publisher = self.create_publisher(Image, 'camera/image', 10)
        
        self.timer = self.create_timer(0.033, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('图像发布器已启动')
        self.get_logger().info('在RViz中添加Image显示，话题: /camera/image')
    
    def timer_callback(self):
        img = self.create_image()
        msg = self.cv2_to_imgmsg(img)
        self.publisher.publish(msg)
        
        self.counter += 1
    
    def create_image(self):
        height, width = 480, 640
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        img[:, :] = (50, 50, 50)
        
        center_x = int(width / 2 + 100 * np.sin(self.counter * 0.05))
        center_y = int(height / 2 + 100 * np.cos(self.counter * 0.05))
        radius = 50
        color = (0, 255, 0)
        cv2.circle(img, (center_x, center_y), radius, color, -1)
        
        cv2.rectangle(img, (50, 50), (150, 150), (255, 0, 0), 2)
        
        pts = np.array([
            [300, 100],
            [400, 150],
            [350, 200],
            [250, 200]
        ], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (0, 0, 255), 2)
        
        text = f"Frame: {self.counter}"
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2)
        
        return img
    
    def cv2_to_imgmsg(self, cv_image):
        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_link"
        msg.height = cv_image.shape[0]
        msg.width = cv_image.shape[1]
        msg.encoding = "bgr8"
        msg.is_bigendian = 0
        msg.step = cv_image.shape[1] * 3
        msg.data = cv_image.tobytes()
        return msg


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


if __name__ == '__main__':
    main()
