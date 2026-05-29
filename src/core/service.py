"""
服务类模块
提供打印服务（门面模式）
"""

from .formatter import TextFormatter
from .outputter import ConsoleOutputter
from .problem_set import ProblemSet
from .interfaces import IFormatter, IOutputter


class ProblemPrintService:
    """问题打印服务 - 组合格式化器和输出器

    设计模式：门面模式
    提供简化的接口，隐藏复杂的格式化和输出逻辑

    职责：协调格式化和输出

    Attributes:
        _formatter: 格式化器
        _outputter: 输出器
    """

    def __init__(self, formatter: IFormatter, outputter: IOutputter):
        self._formatter = formatter
        self._outputter = outputter

    def print_problems(self, problem_set: ProblemSet, per_line: int = 5) -> None:
        """打印题目

        Args:
            problem_set: 问题集合
            per_line: 每行显示的题目数量
        """
        content = self._formatter.format_problems(problem_set.get_problems(), per_line)
        self._outputter.output(content)

    def print_answers(self, problem_set: ProblemSet, per_line: int = 5) -> None:
        """打印答案

        Args:
            problem_set: 问题集合
            per_line: 每行显示的答案数量
        """
        content = self._formatter.format_answers(problem_set.get_problems(), per_line)
        self._outputter.output(content)