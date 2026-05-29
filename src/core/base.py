"""
抽象基类模块
定义运算的抽象基类
"""

from abc import ABC, abstractmethod
from typing import Optional
from .types import OperationConfig
from .interfaces import IOperation


class BaseOperation(ABC, IOperation):
    """运算抽象基类 - 提供通用实现和模板方法

    设计模式：模板方法模式
    子类实现具体的calculate方法，基类提供通用行为

    Attributes:
        config: 运算配置
    """

    def __init__(self, config: Optional[OperationConfig] = None):
        self.config = config or OperationConfig(None)

    @abstractmethod
    def calculate(self, a: int, b: int) -> int:
        """子类必须实现具体的计算逻辑"""
        pass

    def get_comparison_key(self, a: int, b: int) -> tuple:
        """模板方法 - 子类可重写，默认实现"""
        return (a, b, self.get_symbol())

    def get_symbol(self) -> str:
        """默认符号，子类可重写"""
        return "?"