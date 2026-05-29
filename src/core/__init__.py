"""
核心模块初始化文件
导出所有公共接口和类
"""

# 类型定义
from .types import OperationType, OperationConfig

# 接口
from .interfaces import (
    IOperation,
    IFormatter,
    IOutputter,
    IIterator,
    IAggregate,
)

# 抽象基类
from .base import BaseOperation

# 具体运算类
from .operations import Addition, Subtraction, Multiplication

# 实体类
from .problem import Problem

# 生成器
from .generator import ProblemGenerator

# 题目集和迭代器
from .problem_set import ProblemSet, ProblemIterator

# 格式化器
from .formatter import TextFormatter

# 输出器
from .outputter import ConsoleOutputter

# 服务
from .service import ProblemPrintService

# 工厂
from .factory import ProblemSetFactory

# 策略管理器
from .strategy import OperationStrategyManager

__all__ = [
    # 类型
    "OperationType",
    "OperationConfig",

    # 接口
    "IOperation",
    "IFormatter",
    "IOutputter",
    "IIterator",
    "IAggregate",

    # 抽象基类
    "BaseOperation",

    # 具体运算类
    "Addition",
    "Subtraction",
    "Multiplication",

    # 实体类
    "Problem",

    # 生成器
    "ProblemGenerator",

    # 题目集和迭代器
    "ProblemSet",
    "ProblemIterator",

    # 格式化器
    "TextFormatter",

    # 输出器
    "ConsoleOutputter",

    # 服务
    "ProblemPrintService",

    # 工厂
    "ProblemSetFactory",

    # 策略管理器
    "OperationStrategyManager",
]