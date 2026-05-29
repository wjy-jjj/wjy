"""
口算练习题生成器 - 完整版本
面向对象设计，遵循SOLID原则

核心特性：
- 抽象：使用抽象基类定义运算接口
- 封装：类封装数据和行为，隐藏内部实现
- 多态：不同运算类型统一处理，可扩展
- 继承：具体运算类继承抽象基类

设计模式：
- 策略模式：IOperation及其实现类
- 工厂模式：ProblemSetFactory
- 迭代器模式：ProblemIterator
- 模板方法模式：BaseOperation
"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Set, Optional, Iterator, Protocol
from dataclasses import dataclass


# ========================================
# 抽象数据类型 - 运算类型枚举
# ========================================
class OperationType(Enum):
    """运算类型枚举 - 抽象数据类型"""
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()  # 预留扩展
    DIVISION = auto()        # 预留扩展


# ========================================
# 数据传输对象 - 运算配置
# ========================================
@dataclass
class OperationConfig:
    """运算配置数据类 - 数据传输对象"""
    operation_type: OperationType
    min_value: int = 1
    max_value: int = 99
    max_result: int = 100
    min_result: int = 0


# ========================================
# 抽象基类 - 运算接口（协议形式）
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
    def get_operation_type(self) -> OperationType:
        """获取运算类型"""
        pass

    @abstractmethod
    def get_comparison_key(self, a: int, b: int) -> tuple:
        """获取比较键 - 用于去重，多态实现"""
        pass


# ========================================
# 抽象基类 - 运算基类（模板方法模式）
# ========================================
class BaseOperation(ABC, IOperation):
    """运算抽象基类 - 提供通用实现和模板方法

    设计模式：模板方法模式
    子类实现具体的calculate方法，基类提供通用行为
    """

    def __init__(self, config: Optional[OperationConfig] = None):
        self.config = config or OperationConfig(OperationType.ADDITION)

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


# ========================================
# 具体运算类 - 策略模式的具体策略
# ========================================
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


# 预留扩展：乘法和除法运算
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


# ========================================
# 实体类 - 算式问题
# ========================================
class Problem:
    """算式问题类 - 封装数据和行为

    职责：表示一道算式，提供相关操作
    单一职责原则：只负责问题本身，不负责生成、存储或打印
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

    def equals(self, other: Problem) -> bool:
        """判断两个问题是否相同（数值上）"""
        return self.get_key() == other.get_key()


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
    def next(self) -> Problem:
        """获取下一个元素"""
        pass


# ========================================
# 迭代器模式 - 问题集迭代器
# ========================================
class ProblemIterator:
    """问题集迭代器 - 迭代器模式实现

    职责：提供对问题集的迭代访问
    单一职责原则：只负责迭代，不负责数据存储或格式化
    """

    def __init__(self, problems: List[Problem]):
        self._problems = problems
        self._position = 0

    def has_next(self) -> bool:
        """是否还有下一个元素"""
        return self._position < len(self._problems)

    def next(self) -> Problem:
        """获取下一个元素"""
        if not self.has_next():
            raise StopIteration("没有更多元素")
        problem = self._problems[self._position]
        self._position += 1
        return problem

    def reset(self) -> None:
        """重置迭代器"""
        self._position = 0


# ========================================
# 聚合接口
# ========================================
class IAggregate(Protocol):
    """聚合接口 - 迭代器模式"""

    @abstractmethod
    def create_iterator(self) -> IIterator:
        """创建迭代器"""
        pass


# ========================================
# 生成器类 - 生成不重复问题
# ========================================
class ProblemGenerator:
    """问题生成器 - 生成不重复的算式

    职责：根据配置生成问题，确保不重复
    单一职责原则：只负责生成，不负责存储、格式化或验证业务规则

    依赖：依赖IOperation抽象接口，而非具体实现
    """

    def __init__(self, operations: List[IOperation]):
        if not operations:
            raise ValueError("至少需要一个运算类型")
        self._operations = operations

    def generate(self, count: int) -> List[Problem]:
        """生成指定数量的不重复问题"""
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
        """生成单个问题"""
        operation = random.choice(self._operations)

        while True:
            a = random.randint(1, 99)
            b = random.randint(1, 99)
            if operation.is_valid(a, b):
                return Problem(a, b, operation)


# ========================================
# 集合类 - 问题集
# ========================================
class ProblemSet(IAggregate):
    """题目集合 - 管理问题集，支持迭代

    职责：管理问题集合，提供迭代和统计功能
    单一职责原则：只负责管理和提供访问，不负责格式化输出
    """

    def __init__(self, problems: List[Problem]):
        self._problems = problems

    def create_iterator(self) -> ProblemIterator:
        """创建迭代器 - 迭代器模式"""
        return ProblemIterator(self._problems)

    def get_problems(self) -> List[Problem]:
        """获取所有问题"""
        return self._problems.copy()

    def count(self) -> int:
        """获取问题数量"""
        return len(self._problems)

    def count_by_operation(self, operation_type: OperationType) -> int:
        """按运算类型统计数量"""
        return sum(
            1 for p in self._problems
            if p.operation.get_operation_type() == operation_type
        )

    def add(self, problem: Problem) -> None:
        """添加问题"""
        self._problems.append(problem)

    def remove(self, problem: Problem) -> bool:
        """移除问题"""
        try:
            self._problems.remove(problem)
            return True
        except ValueError:
            return False

    def __len__(self) -> int:
        return len(self._problems)

    def __iter__(self) -> Iterator[Problem]:
        """支持Python原生迭代"""
        return iter(self._problems)

    def __getitem__(self, index: int) -> Problem:
        """支持索引访问"""
        return self._problems[index]


# ========================================
# 格式化器接口 - 分离格式化逻辑
# ========================================
class IFormatter(Protocol):
    """格式化器接口"""

    @abstractmethod
    def format_problems(self, problems: List[Problem], per_line: int) -> str:
        """格式化题目"""
        pass

    @abstractmethod
    def format_answers(self, problems: List[Problem], per_line: int) -> str:
        """格式化答案"""
        pass


# ========================================
# 具体格式化器 - 文本格式化器
# ========================================
class TextFormatter:
    """文本格式化器 - 实现格式化接口

    职责：将问题集格式化为文本输出
    单一职责原则：只负责格式化，不负责业务逻辑
    """

    def format_problems(self, problems: List[Problem], per_line: int = 5) -> str:
        """格式化题目为文本"""
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
        """格式化答案为文本"""
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


# ========================================
# 输出器接口 - 分离输出逻辑
# ========================================
class IOutputter(Protocol):
    """输出器接口"""

    @abstractmethod
    def output(self, content: str) -> None:
        """输出内容"""
        pass


# ========================================
# 具体输出器 - 控制台输出器
# ========================================
class ConsoleOutputter:
    """控制台输出器 - 实现输出接口

    职责：将内容输出到控制台
    单一职责原则：只负责输出
    """

    def output(self, content: str) -> None:
        """输出内容到控制台"""
        print(content)


# ========================================
# 服务类 - 打印服务（门面模式）
# ========================================
class ProblemPrintService:
    """问题打印服务 - 组合格式化器和输出器

    设计模式：门面模式
    提供简化的接口，隐藏复杂的格式化和输出逻辑

    职责：协调格式化和输出
    """

    def __init__(self, formatter: IFormatter, outputter: IOutputter):
        self._formatter = formatter
        self._outputter = outputter

    def print_problems(self, problem_set: ProblemSet, per_line: int = 5) -> None:
        """打印题目"""
        content = self._formatter.format_problems(problem_set.get_problems(), per_line)
        self._outputter.output(content)

    def print_answers(self, problem_set: ProblemSet, per_line: int = 5) -> None:
        """打印答案"""
        content = self._formatter.format_answers(problem_set.get_problems(), per_line)
        self._outputter.output(content)


# ========================================
# 工厂模式 - 工厂类（简单工厂）
# ========================================
class ProblemSetFactory:
    """题目集工厂 - 创建不同配置的题目集

    设计模式：简单工厂模式
    集中管理对象的创建逻辑

    职责：根据需求创建不同配置的问题集
    """

    @staticmethod
    def create_standard_set(count: int = 50) -> ProblemSet:
        """创建标准题目集：50题，加减法混合"""
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_addition_only(count: int = 50) -> ProblemSet:
        """创建仅加法的题目集"""
        operations = [Addition()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_subtraction_only(count: int = 50) -> ProblemSet:
        """创建仅减法的题目集"""
        operations = [Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_multiplication_set(count: int = 50) -> ProblemSet:
        """创建乘法题目集"""
        operations = [Multiplication()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_custom_set(count: int, operations: List[IOperation]) -> ProblemSet:
        """创建自定义题目集 - 扩展点"""
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)

    @staticmethod
    def create_mixed_set(count: int, include_multiplication: bool = False) -> ProblemSet:
        """创建混合运算题目集"""
        operations = [Addition(), Subtraction()]
        if include_multiplication:
            operations.append(Multiplication())
        generator = ProblemGenerator(operations)
        problems = generator.generate(count)
        return ProblemSet(problems)


# ========================================
# 策略模式 - 运算策略管理器
# ========================================
class OperationStrategyManager:
    """运算策略管理器 - 策略模式的上下文类

    设计模式：策略模式
    管理不同的运算策略，运行时可切换

    职责：管理运算策略的注册和使用
    """

    def __init__(self):
        self._strategies: dict[OperationType, type[IOperation]] = {}
        self._register_default_strategies()

    def _register_default_strategies(self) -> None:
        """注册默认策略"""
        self.register(OperationType.ADDITION, Addition)
        self.register(OperationType.SUBTRACTION, Subtraction)
        self.register(OperationType.MULTIPLICATION, Multiplication)

    def register(self, operation_type: OperationType, strategy_class: type[IOperation]) -> None:
        """注册新的运算策略"""
        self._strategies[operation_type] = strategy_class

    def create_strategy(self, operation_type: OperationType) -> IOperation:
        """创建运算策略实例"""
        if operation_type not in self._strategies:
            raise ValueError(f"不支持的运算类型: {operation_type}")
        return self._strategies[operation_type]()

    def get_available_types(self) -> List[OperationType]:
        """获取可用的运算类型"""
        return list(self._strategies.keys())


# ========================================
# 主程序
# ========================================
def main():
    """主程序入口"""
    print("口算练习题生成器 v2.0")
    print("面向对象设计 | SOLID原则 | 设计模式")
    print("-" * 60)

    # 使用工厂创建标准题目集
    problem_set = ProblemSetFactory.create_standard_set()

    # 创建打印服务（依赖注入）
    formatter = TextFormatter()
    outputter = ConsoleOutputter()
    print_service = ProblemPrintService(formatter, outputter)

    # 打印题目
    print_service.print_problems(problem_set, per_line=5)

    # 打印答案
    print_service.print_answers(problem_set, per_line=5)

    # 统计信息
    print("\n统计信息:")
    print(f"- 总题数: {problem_set.count()}")
    print(f"- 加法题数: {problem_set.count_by_operation(OperationType.ADDITION)}")
    print(f"- 减法题数: {problem_set.count_by_operation(OperationType.SUBTRACTION)}")

    # 演示迭代器模式
    print("\n迭代器演示（前5题）:")
    iterator = problem_set.create_iterator()
    for _ in range(min(5, problem_set.count())):
        if iterator.has_next():
            print(f"  {iterator.next()}")

    # 演示策略模式
    print("\n策略模式演示:")
    strategy_manager = OperationStrategyManager()
    addition_strategy = strategy_manager.create_strategy(OperationType.ADDITION)
    print(f"  创建的加法策略: {addition_strategy}")
    print(f"  可用策略: {[t.name for t in strategy_manager.get_available_types()]}")


if __name__ == "__main__":
    main()