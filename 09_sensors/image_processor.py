#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2


class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        
        self.subscription = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10
        )
        
        self.processed_pub = self.create_publisher(Image, 'camera/image_processed', 10)
        
        self.get_logger().info('图像处理器已启动')
    
    def image_callback(self, msg):
        cv_image = self.imgmsg_to_cv2(msg)
        
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        result = cv_image.copy()
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            
            M = cv2.moments(largest_contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                
                cv2.circle(result, (cx, cy), 5, (0, 255, 0), -1)
                
                cv2.drawContours(result, [largest_contour], -1, (0, 255, 0), 2)
                
                text = f"Target: ({cx}, {cy})"
                cv2.putText(result, text, (cx + 10, cy - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                self.get_logger().info(f'检测到红色目标: ({cx}, {cy})')
        
        processed_msg = self.cv2_to_imgmsg(result)
        self.processed_pub.publish(processed_msg)
    
    def imgmsg_to_cv2(self, msg):
        dtype = np.uint8
        img = np.frombuffer(msg.data, dtype=dtype).reshape(msg.height, msg.width, -1)
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
    node = ImageProcessor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
