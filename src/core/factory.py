"""
工厂类模块
负责创建不同配置的题目集（工厂模式）
"""

from typing import List
from .interfaces import IOperation
from .generator import ProblemGenerator
from .problem_set import ProblemSet
from .operations import Addition, Subtraction, Multiplication


class ProblemSetFactory:
    """题目集工厂 - 创建不同配置的题目集

    设计模式：简单工厂模式
    集中管理对象的创建逻辑

    职责：根据需求创建不同配置的问题集
    """

    @staticmethod
    def create_standard_set(count: int = 50) -> ProblemSet:
        """创建标准题目集：50题，加减法混合

        Args:
            count: 要生成的题目数量

        Returns:
            问题集
        """
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_addition_only(count: int = 50) -> ProblemSet:
        """创建仅加法的题目集

        Args:
            count: 要生成的题目数量

        Returns:
            问题集
        """
        operations = [Addition()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_subtraction_only(count: int = 50) -> ProblemSet:
        """创建仅减法的题目集

        Args:
            count: 要生成的题目数量

        Returns:
            问题集
        """
        operations = [Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_multiplication_set(count: int = 50) -> ProblemSet:
        """创建乘法题目集

        Args:
            count: 要生成的题目数量

        Returns:
            问题集
        """
        operations = [Multiplication()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_custom_set(count: int, operations: List[IOperation]) -> ProblemSet:
        """创建自定义题目集 - 扩展点

        Args:
            count: 要生成的题目数量
            operations: 可用的运算类型列表

        Returns:
            问题集
        """
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_mixed_set(count: int, include_multiplication: bool = False) -> ProblemSet:
        """创建混合运算题目集

        Args:
            count: 要生成的题目数量
            include_multiplication: 是否包含乘法

        Returns:
            问题集
        """
        operations = [Addition(), Subtraction()]
        if include_multiplication:
            operations.append(Multiplication())
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)