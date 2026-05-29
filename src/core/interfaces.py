"""
接口定义模块
定义项目中使用的抽象接口
"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Iterator, TYPE_CHECKING

# 使用TYPE_CHECKING避免循环导入
if TYPE_CHECKING:
    from .problem import Problem


# ========================================
# 运算接口
# ========================================
class IOperation(Protocol):
    """运算抽象接口 - 协议形式

    面向接口编程，具体类实现此接口
    """

    @abstractmethod
    def calculate(self, a: int, b: int) -> int:
        """计算结果"""
        pass

    @abstractmethod
    def is_valid(self, a: int, b: int) -> bool:
        """验证运算是否有效"""
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """获取运算符"""
        pass

    @abstractmethod
    def get_operation_type(self):
        """获取运算类型"""
        pass

    @abstractmethod
    def get_comparison_key(self, a: int, b: int) -> tuple:
        """获取比较键 - 用于去重，多态实现"""
        pass


# ========================================
# 格式化器接口
# ========================================
class IFormatter(Protocol):
    """格式化器接口"""

    @abstractmethod
    def format_problems(self, problems: List["Problem"], per_line: int) -> str:
        """格式化题目"""
        pass

    @abstractmethod
    def format_answers(self, problems: List["Problem"], per_line: int) -> str:
        """格式化答案"""
        pass


# ========================================
# 输出器接口
# ========================================
class IOutputter(Protocol):
    """输出器接口"""

    @abstractmethod
    def output(self, content: str) -> None:
        """输出内容"""
        pass


# ========================================
# 迭代器接口
# ========================================
class IIterator(Protocol):
    """迭代器接口"""

    @abstractmethod
    def has_next(self) -> bool:
        """是否还有下一个元素"""
        pass

    @abstractmethod
    def next(self) -> "Problem":
        """获取下一个元素"""
        pass


# ========================================
# 聚合接口
# ========================================
class IAggregate(Protocol):
    """聚合接口 - 迭代器模式"""

    @abstractmethod
    def create_iterator() -> IIterator:
        """创建迭代器"""
        pass