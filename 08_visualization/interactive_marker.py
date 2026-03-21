#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, Marker
from interactive_markers import InteractiveMarkerServer
from geometry_msgs.msg import Point


class InteractiveMarkerNode(Node):
    def __init__(self):
        super().__init__('interactive_marker_node')
        
        self.server = InteractiveMarkerServer(self, 'simple_marker')
        
        self.make_6dof_marker()
        
        self.server.applyChanges()
        
        self.get_logger().info('交互式Marker已启动')
        self.get_logger().info('在RViz中可以拖动Marker')
    
    def make_6dof_marker(self):
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = "base_link"
        int_marker.name = "6dof_marker"
        int_marker.description = "可拖动的6自由度Marker"
        int_marker.scale = 1.0
        
        box_marker = Marker()
        box_marker.type = Marker.CUBE
        box_marker.scale.x = 0.45
        box_marker.scale.y = 0.45
        box_marker.scale.z = 0.45
        box_marker.color.r = 0.5
        box_marker.color.g = 0.5
        box_marker.color.b = 0.5
        box_marker.color.a = 1.0
        
        control = InteractiveMarkerControl()
        control.always_visible = True
        control.markers.append(box_marker)
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 1.0
        control.orientation.y = 0.0
        control.orientation.z = 0.0
        control.name = "rotate_x"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 1.0
        control.orientation.y = 0.0
        control.orientation.z = 0.0
        control.name = "move_x"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 1.0
        control.orientation.z = 0.0
        control.name = "rotate_z"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 1.0
        control.orientation.z = 0.0
        control.name = "move_z"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 0.0
        control.orientation.z = 1.0
        control.name = "rotate_y"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        int_marker.controls.append(control)
        
        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 0.0
        control.orientation.z = 1.0
        control.name = "move_y"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        int_marker.controls.append(control)
        
        self.server.insert(int_marker, feedback_callback=self.process_feedback)
    
    def process_feedback(self, feedback):
        p = feedback.pose.position
        self.get_logger().info(
            f'Marker位置: x={p.x:.2f}, y={p.y:.2f}, z={p.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = InteractiveMarkerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
