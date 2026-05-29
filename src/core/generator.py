"""
生成器类模块
负责生成不重复的算式问题
"""

import random
from typing import List
from .interfaces import IOperation
from .problem import Problem


class ProblemGenerator:
    """问题生成器 - 生成不重复的算式

    职责：根据配置生成问题，确保不重复
    单一职责原则：只负责生成，不负责存储、格式化或验证业务规则

    依赖：依赖IOperation抽象接口，而非具体实现

    Attributes:
        _operations: 可用的运算类型列表
    """

    def __init__(self, operations: List[IOperation]):
        if not operations:
            raise ValueError("至少需要一个运算类型")
        self._operations = operations

    def generate(self, count: int) -> List[Problem]:
        """生成指定数量的不重复问题

        Args:
            count: 要生成的问题数量

        Returns:
            生成的问题列表
        """
        if count <= 0:
            return []

        problems = []
        seen_keys = set()
        attempts = 0
        max_attempts = count * 100  # 防止无限循环

        while len(problems) < count and attempts < max_attempts:
            problem = self._generate_single()
            key = problem.get_key()

            if key not in seen_keys:
                seen_keys.add(key)
                problems.append(problem)

            attempts += 1

        if len(problems) < count:
            print(f"警告: 仅生成 {len(problems)} 道题（目标 {count} 道）")

        return problems

    def _generate_single(self) -> Problem:
        """生成单个问题

        Returns:
            单个问题实例
        """
        operation = random.choice(self._operations)

        while True:
            a = random.randint(1, 99)
            b = random.randint(1, 99)
            if operation.is_valid(a, b):
                return Problem(a, b, operation)