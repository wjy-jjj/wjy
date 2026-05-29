"""
输出器类模块
负责将内容输出到控制台
"""

from .interfaces import IOutputter


class ConsoleOutputter:
    """控制台输出器 - 实现输出接口

    职责：将内容输出到控制台
    单一职责原则：只负责输出

    Methods:
        output: 输出内容到控制台
    """

    def output(self, content: str) -> None:
        """输出内容到控制台

        Args:
            content: 要输出的内容
        """
        print(content)