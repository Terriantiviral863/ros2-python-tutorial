#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

/**
 * 简单的C++发布者节点示例
 * 演示如何在ROS2 C++包中创建发布者
 */
class SimplePublisher : public rclcpp::Node
{
public:
  SimplePublisher()
  : Node("simple_publisher"), counter_(0)
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("example_topic", 10);
    
    timer_ = this->create_wall_timer(
      1000ms, std::bind(&SimplePublisher::timer_callback, this));
    
    RCLCPP_INFO(this->get_logger(), "C++简单发布者节点已启动");
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "来自C++包的消息 #" + std::to_string(counter_);
    
    publisher_->publish(message);
    RCLCPP_INFO(this->get_logger(), "发布: '%s'", message.data.c_str());
    
    counter_++;
  }
  
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  size_t counter_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SimplePublisher>());
  rclcpp::shutdown();
  return 0;
}
