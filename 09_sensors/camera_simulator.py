#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2


class CameraSimulator(Node):
    def __init__(self):
        super().__init__('camera_simulator')
        
        self.publisher = self.create_publisher(Image, 'camera/image_raw', 10)
        
        self.timer = self.create_timer(0.033, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('相机模拟器已启动')
        self.get_logger().info('发布图像到: /camera/image_raw')
    
    def timer_callback(self):
        height, width = 480, 640
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        img[:, :] = (100, 150, 200)
        
        ball_x = int(width / 2 + 150 * np.sin(self.counter * 0.05))
        ball_y = int(height / 2 + 100 * np.cos(self.counter * 0.05))
        cv2.circle(img, (ball_x, ball_y), 30, (0, 0, 255), -1)
        
        cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), 3)
        
        cv2.line(img, (0, height//2), (width, height//2), (255, 255, 255), 1)
        cv2.line(img, (width//2, 0), (width//2, height), (255, 255, 255), 1)
        
        text = f"Frame: {self.counter}"
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2)
        
        msg = self.cv2_to_imgmsg(img)
        self.publisher.publish(msg)
        
        self.counter += 1
    
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
    node = CameraSimulator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
