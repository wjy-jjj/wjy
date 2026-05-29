"""
策略管理器模块
负责管理运算策略（策略模式）
"""

from typing import List, Type
from .interfaces import IOperation
from .types import OperationType
from .operations import Addition, Subtraction, Multiplication


class OperationStrategyManager:
    """运算策略管理器 - 策略模式的上下文类

    设计模式：策略模式
    管理不同的运算策略，运行时可切换

    职责：管理运算策略的注册和使用

    Attributes:
        _strategies: 策略字典，映射运算类型到策略类
    """

    def __init__(self):
        self._strategies: dict[OperationType, type[IOperation]] = {}
        self._register_default_strategies()

    def _register_default_strategies(self) -> None:
        """注册默认策略"""
        self.register(OperationType.ADDITION, Addition)
        self.register(OperationType.SUBTRACTION, Subtraction)
        self.register(OperationType.MULTIPLICATION, Multiplication)

    def register(self, operation_type: OperationType, strategy_class: type[IOperation]) -> None:
        """注册新的运算策略

        Args:
            operation_type: 运算类型
            strategy_class: 策略类
        """
        self._strategies[operation_type] = strategy_class

    def create_strategy(self, operation_type: OperationType) -> IOperation:
        """创建运算策略实例

        Args:
            operation_type: 运算类型

        Returns:
            运算策略实例

        Raises:
            ValueError: 当运算类型不支持时
        """
        if operation_type not in self._strategies:
            raise ValueError(f"不支持的运算类型: {operation_type}")
        return self._strategies[operation_type]()

    def get_available_types(self) -> List[OperationType]:
        """获取可用的运算类型

        Returns:
            可用的运算类型列表
        """
        return list(self._strategies.keys())