# 传感器数据消息

# 标准消息头
std_msgs/Header header

# 传感器类型
string sensor_type

# 传感器ID
int32 sensor_id

# 数据值数组
float64[] values

# 数据质量 (0.0-1.0)
float32 quality

# 是否有效
bool is_valid
