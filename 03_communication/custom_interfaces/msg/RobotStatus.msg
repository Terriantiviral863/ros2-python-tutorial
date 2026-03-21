# 机器人状态消息

# 标准消息头
std_msgs/Header header

# 机器人ID
string robot_id

# 状态 (IDLE, RUNNING, PAUSED, ERROR, CHARGING)
string status

# 电池电量 (0-100)
float32 battery_level

# 位置
geometry_msgs/Point position

# 速度 (m/s)
float32 velocity

# 是否在执行任务
bool is_busy

# 错误代码 (0表示无错误)
int32 error_code

# 额外信息
string message
