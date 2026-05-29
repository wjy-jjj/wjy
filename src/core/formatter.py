"""
格式化器类模块
负责将问题集格式化为文本输出
"""

from typing import List
from .problem import Problem
from .interfaces import IFormatter


class TextFormatter:
    """文本格式化器 - 实现格式化接口

    职责：将问题集格式化为文本输出
    单一职责原则：只负责格式化，不负责业务逻辑

    Methods:
        format_problems: 格式化题目
        format_answers: 格式化答案
    """

    def format_problems(self, problems: List[Problem], per_line: int = 5) -> str:
        """格式化题目为文本

        Args:
            problems: 问题列表
            per_line: 每行显示的题目数量

        Returns:
            格式化后的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("口算练习题")
        lines.append("=" * 60)

        line_buffer = []
        for problem in problems:
            line_buffer.append(str(problem))
            if len(line_buffer) >= per_line:
                lines.append("  ".join(line_buffer))
                line_buffer = []

        if line_buffer:
            lines.append("  ".join(line_buffer))

        lines.append("=" * 60)
        lines.append(f"共 {len(problems)} 道题")
        lines.append("=" * 60)

        return "\n".join(lines)

    def format_answers(self, problems: List[Problem], per_line: int = 5) -> str:
        """格式化答案为文本

        Args:
            problems: 问题列表
            per_line: 每行显示的答案数量

        Returns:
            格式化后的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("参考答案")
        lines.append("=" * 60)

        line_buffer = []
        for problem in problems:
            line_buffer.append(problem.with_answer())
            if len(line_buffer) >= per_line:
                lines.append("  ".join(line_buffer))
                line_buffer = []

        if line_buffer:
            lines.append("  ".join(line_buffer))

        lines.append("=" * 60)

        return "\n".join(lines)