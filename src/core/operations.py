"""
具体运算类模块
包含加法、减法、乘法运算的实现
"""

from typing import Optional
from .base import BaseOperation
from .types import OperationConfig, OperationType


class Addition(BaseOperation):
    """加法运算 - 策略模式的具体策略实现"""

    def __init__(self, config: Optional[OperationConfig] = None):
        if config is None:
            config = OperationConfig(OperationType.ADDITION, max_result=100)
        super().__init__(config)

    def calculate(self, a: int, b: int) -> int:
        return a + b

    def is_valid(self, a: int, b: int) -> bool:
        """加法结果不能超过100"""
        result = self.calculate(a, b)
        return self.config.min_value <= a <= self.config.max_value and \
               self.config.min_value <= b <= self.config.max_value and \
               self.config.min_result <= result <= self.config.max_result

    def get_symbol(self) -> str:
        return "+"

    def get_operation_type(self) -> OperationType:
        return OperationType.ADDITION

    def get_comparison_key(self, a: int, b: int) -> tuple:
        """加法：顺序无关，用排序后的元组"""
        return (min(a, b), max(a, b), self.get_symbol())


class Subtraction(BaseOperation):
    """减法运算 - 策略模式的具体策略实现"""

    def __init__(self, config: Optional[OperationConfig] = None):
        if config is None:
            config = OperationConfig(OperationType.SUBTRACTION, min_result=0)
        super().__init__(config)

    def calculate(self, a: int, b: int) -> int:
        return a - b

    def is_valid(self, a: int, b: int) -> bool:
        """减法结果不能小于0"""
        result = self.calculate(a, b)
        return self.config.min_value <= a <= self.config.max_value and \
               self.config.min_value <= b <= self.config.max_value and \
               self.config.min_result <= result <= self.config.max_result

    def get_symbol(self) -> str:
        return "-"

    def get_operation_type(self) -> OperationType:
        return OperationType.SUBTRACTION

    def get_comparison_key(self, a: int, b: int) -> tuple:
        """减法：顺序有关"""
        return (a, b, self.get_symbol())


class Multiplication(BaseOperation):
    """乘法运算 - 预留扩展"""

    def __init__(self, config: Optional[OperationConfig] = None):
        if config is None:
            config = OperationConfig(OperationType.MULTIPLICATION, max_value=9, max_result=81)
        super().__init__(config)

    def calculate(self, a: int, b: int) -> int:
        return a * b

    def is_valid(self, a: int, b: int) -> bool:
        result = self.calculate(a, b)
        return self.config.min_value <= a <= self.config.max_value and \
               self.config.min_value <= b <= self.config.max_value and \
               self.config.min_result <= result <= self.config.max_result

    def get_symbol(self) -> str:
        return "×"

    def get_operation_type(self) -> OperationType:
        return OperationType.MULTIPLICATION