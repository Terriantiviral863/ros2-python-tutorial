# 贡献指南

感谢你对ROS2 Python教程项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果你发现了bug或有改进建议：

1. 在GitHub Issues中搜索，确保问题尚未被报告
2. 创建新的Issue，清晰描述问题
3. 包含复现步骤、预期行为和实际行为
4. 如果可能，提供代码示例或截图

### 提交代码

1. **Fork项目**
   ```bash
   # 在GitHub上Fork项目
   # 克隆你的Fork
   git clone https://github.com/your-username/ros2-python-tutorial.git
   cd ros2-python-tutorial
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **编写代码**
   - 遵循现有代码风格
   - 添加必要的注释
   - 确保代码可运行
   - 更新相关文档

4. **测试代码**
   ```bash
   # 运行你的代码确保正常工作
   python3 your_script.py
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复bug描述"
   ```

6. **推送到GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 在GitHub上创建Pull Request
   - 清晰描述你的更改
   - 关联相关的Issue

## 代码规范

### Python代码风格

- 遵循PEP 8规范
- 使用4个空格缩进
- 函数和变量使用snake_case
- 类名使用PascalCase
- 添加docstring说明

示例：
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class MyNode(Node):
    """
    节点功能描述
    """
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('节点已启动')
    
    def my_function(self, param):
        """
        函数功能描述
        
        Args:
            param: 参数说明
        
        Returns:
            返回值说明
        """
        pass
```

### 文档规范

- README使用Markdown格式
- 代码注释使用中文
- 提供清晰的使用示例
- 包含必要的运行命令

## 提交信息规范

使用语义化的提交信息：

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: 添加激光雷达数据处理示例
fix: 修复TF监听器的时间戳问题
docs: 更新导航系统README
```

## 贡献方向

我们特别欢迎以下方向的贡献：

### 代码示例
- 新的ROS2功能示例
- 更好的代码实现
- 性能优化

### 文档改进
- 修正错误
- 补充说明
- 添加图表
- 翻译成其他语言

### 新功能
- 新的学习模块
- 实用工具脚本
- 可视化工具

### 测试
- 单元测试
- 集成测试
- 测试文档

## 行为准则

- 尊重所有贡献者
- 欢迎建设性的批评
- 专注于对项目最有利的事情
- 展现同理心

## 问题？

如有任何问题，欢迎：
- 创建Issue讨论
- 发送邮件联系维护者
- 在Pull Request中提问

感谢你的贡献！🎉
