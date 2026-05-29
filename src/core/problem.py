"""
问题实体类模块
表示一道算式问题
"""

from .interfaces import IOperation


class Problem:
    """算式问题类 - 封装数据和行为

    职责：表示一道算式，提供相关操作
    单一职责原则：只负责问题本身，不负责生成、存储或打印

    Attributes:
        _a: 第一个操作数（私有）
        _b: 第二个操作数（私有）
        _operation: 运算对象（私有）
        _answer: 答案（私有）
    """

    def __init__(self, a: int, b: int, operation: IOperation):
        self._a = a
        self._b = b
        self._operation = operation
        self._answer = operation.calculate(a, b)

    @property
    def a(self) -> int:
        """第一个操作数 - 只读属性"""
        return self._a

    @property
    def b(self) -> int:
        """第二个操作数 - 只读属性"""
        return self._b

    @property
    def operation(self) -> IOperation:
        """运算对象 - 只读属性"""
        return self._operation

    @property
    def answer(self) -> int:
        """答案 - 只读属性，计算后不可变"""
        return self._answer

    def __str__(self) -> str:
        return f"{self.a} {self.operation.get_symbol()} {self.b} = "

    def __repr__(self) -> str:
        return f"Problem({self.a}, {self.b}, {self.operation.get_symbol()}, {self.answer})"

    def with_answer(self) -> str:
        """带答案的字符串表示"""
        return f"{self.a} {self.operation.get_symbol()} {self.b} = {self.answer}"

    def get_key(self) -> tuple:
        """获取唯一标识 - 用于去重

        使用多态：调用operation.get_comparison_key()而非isinstance检查
        这符合依赖倒转原则，不依赖具体实现
        """
        return self._operation.get_comparison_key(self._a, self._b)

    def equals(self, other: 'Problem') -> bool:
        """判断两个问题是否相同（数值上）"""
        return self.get_key() == other.get_key()