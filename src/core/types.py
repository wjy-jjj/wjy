"""
类型定义模块
定义项目中使用的抽象数据类型
"""

from enum import Enum, auto
from dataclasses import dataclass


class OperationType(Enum):
    """运算类型枚举 - 抽象数据类型

    用于类型安全地标识不同的运算类型
    """
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()


@dataclass
class OperationConfig:
    """运算配置数据类 - 数据传输对象

    封装运算的配置参数，用于创建运算实例

    Attributes:
        operation_type: 运算类型
        min_value: 操作数最小值
        max_value: 操作数最大值
        max_result: 运算结果最大值
        min_result: 运算结果最小值
    """
    operation_type: OperationType
    min_value: int = 1
    max_value: int = 99
    max_result: int = 100
    min_result: int = 0