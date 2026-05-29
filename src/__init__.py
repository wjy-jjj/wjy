"""
口算练习题生成器 - 核心模块
"""

from .core import (
    # 类型
    OperationType,
    OperationConfig,

    # 接口
    IOperation,
    IFormatter,
    IOutputter,
    IIterator,
    IAggregate,

    # 抽象基类
    BaseOperation,

    # 具体运算类
    Addition,
    Subtraction,
    Multiplication,

    # 实体类
    Problem,

    # 生成器
    ProblemGenerator,

    # 题目集和迭代器
    ProblemSet,
    ProblemIterator,

    # 格式化器
    TextFormatter,

    # 输出器
    ConsoleOutputter,

    # 服务
    ProblemPrintService,

    # 工厂
    ProblemSetFactory,

    # 策略管理器
    OperationStrategyManager,
)

__all__ = [
    "OperationType",
    "OperationConfig",
    "IOperation",
    "IFormatter",
    "IOutputter",
    "IIterator",
    "IAggregate",
    "BaseOperation",
    "Addition",
    "Subtraction",
    "Multiplication",
    "Problem",
    "ProblemGenerator",
    "ProblemSet",
    "ProblemIterator",
    "TextFormatter",
    "ConsoleOutputter",
    "ProblemPrintService",
    "ProblemSetFactory",
    "OperationStrategyManager",
]