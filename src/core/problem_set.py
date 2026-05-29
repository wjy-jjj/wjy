"""
问题集合类模块
包含ProblemSet和ProblemIterator
"""

from typing import List, Iterator
from .problem import Problem
from .interfaces import IIterator, IAggregate
from .types import OperationType


# ========================================
# 迭代器类
# ========================================
class ProblemIterator:
    """问题集迭代器 - 迭代器模式实现

    职责：提供对问题集的迭代访问
    单一职责原则：只负责迭代，不负责数据存储或格式化

    Attributes:
        _problems: 问题列表
        _position: 当前迭代位置
    """

    def __init__(self, problems: List[Problem]):
        self._problems = problems
        self._position = 0

    def has_next(self) -> bool:
        """是否还有下一个元素

        Returns:
            是否有下一个元素
        """
        return self._position < len(self._problems)

    def next(self) -> Problem:
        """获取下一个元素

        Returns:
            下一个问题

        Raises:
            StopIteration: 当没有更多元素时
        """
        if not self.has_next():
            raise StopIteration("没有更多元素")
        problem = self._problems[self._position]
        self._position += 1
        return problem

    def reset(self) -> None:
        """重置迭代器"""
        self._position = 0


# ========================================
# 问题集合类
# ========================================
class ProblemSet(IAggregate):
    """题目集合 - 管理问题集，支持迭代

    职责：管理问题集合，提供迭代和统计功能
    单一职责原则：只负责管理和提供访问，不负责格式化输出

    Attributes:
        _problems: 问题列表
    """

    def __init__(self, problems: List[Problem]):
        self._problems = problems

    def create_iterator(self) -> ProblemIterator:
        """创建迭代器 - 迭代器模式

        Returns:
            问题集迭代器
        """
        return ProblemIterator(self._problems)

    def get_problems(self) -> List[Problem]:
        """获取所有问题

        Returns:
            问题列表的副本
        """
        return self._problems.copy()

    def count(self) -> int:
        """获取问题数量

        Returns:
            问题数量
        """
        return len(self._problems)

    def count_by_operation(self, operation_type: OperationType) -> int:
        """按运算类型统计数量

        Args:
            operation_type: 运算类型

        Returns:
            该运算类型的问题数量
        """
        return sum(
            1 for p in self._problems
            if p.operation.get_operation_type() == operation_type
        )

    def add(self, problem: Problem) -> None:
        """添加问题

        Args:
            problem: 要添加的问题
        """
        self._problems.append(problem)

    def remove(self, problem: Problem) -> bool:
        """移除问题

        Args:
            problem: 要移除的问题

        Returns:
            是否成功移除
        """
        try:
            self._problems.remove(problem)
            return True
        except ValueError:
            return False

    def __len__(self) -> int:
        return len(self._problems)

    def __iter__(self) -> Iterator[Problem]:
        """支持Python原生迭代

        Returns:
            迭代器
        """
        return iter(self._problems)

    def __getitem__(self, index: int) -> Problem:
        """支持索引访问

        Args:
            index: 索引

        Returns:
            指定索引的问题

        Raises:
            IndexError: 索引越界时
        """
        return self._problems[index]