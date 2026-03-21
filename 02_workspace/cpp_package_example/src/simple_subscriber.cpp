#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

/**
 * 简单的C++订阅者节点示例
 * 演示如何在ROS2 C++包中创建订阅者
 */
class SimpleSubscriber : public rclcpp::Node
{
public:
  SimpleSubscriber()
  : Node("simple_subscriber")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "example_topic", 10,
      std::bind(&SimpleSubscriber::topic_callback, this, std::placeholders::_1));
    
    RCLCPP_INFO(this->get_logger(), "C++简单订阅者节点已启动，等待消息...");
  }

private:
  void topic_callback(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "收到消息: '%s'", msg->data.c_str());
  }
  
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SimpleSubscriber>());
  rclcpp::shutdown();
  return 0;
}
