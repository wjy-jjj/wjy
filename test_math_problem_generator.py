"""
口算练习题生成器单元测试
使用pytest框架

测试覆盖：
- 运算类的功能测试
- 问题类的功能测试
- 生成器的功能测试
- 题目集的功能测试
- 格式化器的功能测试
- 工厂模式测试
- 策略模式测试
- 迭代器模式测试
"""

import pytest
from math_problem_generator import (
    # 枚举和类型
    OperationType,
    OperationConfig,
    # 运算类
    IOperation,
    BaseOperation,
    Addition,
    Subtraction,
    Multiplication,
    # 问题类
    Problem,
    # 生成器
    ProblemGenerator,
    # 题目集和迭代器
    ProblemSet,
    ProblemIterator,
    # 格式化器
    TextFormatter,
    IFormatter,
    ConsoleOutputter,
    IOutputter,
    ProblemPrintService,
    # 工厂
    ProblemSetFactory,
    # 策略管理器
    OperationStrategyManager,
)


# ========================================
# 测试数据
# ========================================
class TestData:
    """测试数据集"""

    # 加法测试数据
    ADDITION_VALID_CASES = [
        ((10, 20), 30),
        ((50, 49), 99),
        ((1, 99), 100),
        ((33, 33), 66),
    ]

    ADDITION_INVALID_CASES = [
        ((60, 50), 110),  # 超过100
        ((80, 30), 110),  # 超过100
        ((100, 10), 110),  # 超出范围
    ]

    # 减法测试数据
    SUBTRACTION_VALID_CASES = [
        ((100, 50), 50),
        ((50, 30), 20),
        ((99, 1), 98),
        ((10, 10), 0),
    ]

    SUBTRACTION_INVALID_CASES = [
        ((10, 20), -10),  # 负数
        ((5, 10), -5),    # 负数
    ]

    # 乘法测试数据
    MULTIPLICATION_VALID_CASES = [
        ((5, 5), 25),
        ((9, 9), 81),
        ((3, 7), 21),
    ]

    # 去重测试数据
    DUPLICATE_ADDITION_CASES = [
        ((20, 30), (30, 20)),  # 交换操作数，应该被视为重复
        ((10, 40), (40, 10)),
    ]

    NOT_DUPLICATE_SUBTRACTION_CASES = [
        ((50, 30), (30, 50)),  # 减法顺序有关，不是重复
    ]


# ========================================
# 加法运算测试
# ========================================
class TestAddition:
    """加法运算单元测试"""

    @pytest.fixture
    def addition(self):
        """创建加法实例"""
        return Addition()

    def test_calculate_valid_cases(self, addition):
        """测试有效加法计算"""
        for (a, b), expected in TestData.ADDITION_VALID_CASES:
            result = addition.calculate(a, b)
            assert result == expected, f"{a} + {b} = {result}, 期望 {expected}"

    def test_is_valid_valid_cases(self, addition):
        """测试有效加法验证"""
        for (a, b), _ in TestData.ADDITION_VALID_CASES:
            assert addition.is_valid(a, b), f"{a} + {b} 应该是有效的"

    def test_is_valid_invalid_cases(self, addition):
        """测试无效加法验证"""
        for (a, b), _ in TestData.ADDITION_INVALID_CASES:
            assert not addition.is_valid(a, b), f"{a} + {b} 应该是无效的"

    def test_get_symbol(self, addition):
        """测试获取运算符"""
        assert addition.get_symbol() == "+"

    def test_get_operation_type(self, addition):
        """测试获取运算类型"""
        assert addition.get_operation_type() == OperationType.ADDITION

    def test_get_comparison_key_order_independent(self, addition):
        """测试加法比较键与顺序无关"""
        a, b = 20, 30
        key1 = addition.get_comparison_key(a, b)
        key2 = addition.get_comparison_key(b, a)
        assert key1 == key2, "加法的比较键应该与顺序无关"

    def test_custom_config(self):
        """测试自定义配置"""
        config = OperationConfig(OperationType.ADDITION, max_result=50)
        addition = Addition(config)
        assert addition.calculate(25, 24) == 49
        assert addition.is_valid(25, 24)
        assert not addition.is_valid(30, 30)


# ========================================
# 减法运算测试
# ========================================
class TestSubtraction:
    """减法运算单元测试"""

    @pytest.fixture
    def subtraction(self):
        """创建减法实例"""
        return Subtraction()

    def test_calculate_valid_cases(self, subtraction):
        """测试有效减法计算"""
        for (a, b), expected in TestData.SUBTRACTION_VALID_CASES:
            result = subtraction.calculate(a, b)
            assert result == expected, f"{a} - {b} = {result}, 期望 {expected}"

    def test_is_valid_valid_cases(self, subtraction):
        """测试有效减法验证"""
        for (a, b), _ in TestData.SUBTRACTION_VALID_CASES:
            assert subtraction.is_valid(a, b), f"{a} - {b} 应该是有效的"

    def test_is_valid_invalid_cases(self, subtraction):
        """测试无效减法验证"""
        for (a, b), _ in TestData.SUBTRACTION_INVALID_CASES:
            assert not subtraction.is_valid(a, b), f"{a} - {b} 应该是无效的"

    def test_get_symbol(self, subtraction):
        """测试获取运算符"""
        assert subtraction.get_symbol() == "-"

    def test_get_operation_type(self, subtraction):
        """测试获取运算类型"""
        assert subtraction.get_operation_type() == OperationType.SUBTRACTION

    def test_get_comparison_key_order_dependent(self, subtraction):
        """测试减法比较键与顺序有关"""
        a, b = 50, 30
        key1 = subtraction.get_comparison_key(a, b)
        key2 = subtraction.get_comparison_key(b, a)
        assert key1 != key2, "减法的比较键应该与顺序有关"


# ========================================
# 乘法运算测试
# ========================================
class TestMultiplication:
    """乘法运算单元测试"""

    @pytest.fixture
    def multiplication(self):
        """创建乘法实例"""
        return Multiplication()

    def test_calculate_valid_cases(self, multiplication):
        """测试有效乘法计算"""
        for (a, b), expected in TestData.MULTIPLICATION_VALID_CASES:
            result = multiplication.calculate(a, b)
            assert result == expected, f"{a} × {b} = {result}, 期望 {expected}"

    def test_is_valid_valid_cases(self, multiplication):
        """测试有效乘法验证"""
        for (a, b), _ in TestData.MULTIPLICATION_VALID_CASES:
            assert multiplication.is_valid(a, b), f"{a} × {b} 应该是有效的"

    def test_is_valid_invalid_cases(self, multiplication):
        """测试无效乘法验证"""
        assert not multiplication.is_valid(10, 10), "10 × 10 = 100 应该是无效的（默认配置）"

    def test_get_symbol(self, multiplication):
        """测试获取运算符"""
        assert multiplication.get_symbol() == "×"

    def test_get_operation_type(self, multiplication):
        """测试获取运算类型"""
        assert multiplication.get_operation_type() == OperationType.MULTIPLICATION


# ========================================
# 问题类测试
# ========================================
class TestProblem:
    """问题类单元测试"""

    def test_creation(self):
        """测试问题创建"""
        addition = Addition()
        problem = Problem(10, 20, addition)
        assert problem.a == 10
        assert problem.b == 20
        assert problem.answer == 30

    def test_immutability(self):
        """测试属性不可变性"""
        addition = Addition()
        problem = Problem(10, 20, addition)
        with pytest.raises(AttributeError):
            problem.a = 15

    def test_string_representation(self):
        """测试字符串表示"""
        addition = Addition()
        problem = Problem(10, 20, addition)
        assert str(problem) == "10 + 20 = "
        assert problem.with_answer() == "10 + 20 = 30"

    def test_get_key_addition(self):
        """测试加法问题比较键"""
        addition = Addition()
        problem1 = Problem(20, 30, addition)
        problem2 = Problem(30, 20, addition)
        assert problem1.get_key() == problem2.get_key(), "加法交换操作数应该产生相同的键"

    def test_get_key_subtraction(self):
        """测试减法问题比较键"""
        subtraction = Subtraction()
        problem1 = Problem(50, 30, subtraction)
        problem2 = Problem(30, 50, subtraction)
        assert problem1.get_key() != problem2.get_key(), "减法交换操作数应该产生不同的键"

    def test_equals(self):
        """测试问题相等性"""
        addition = Addition()
        problem1 = Problem(20, 30, addition)
        problem2 = Problem(30, 20, addition)
        problem3 = Problem(20, 30, addition)
        assert problem1.equals(problem2), "加法交换操作数应该相等"
        assert problem1.equals(problem3), "相同问题应该相等"


# ========================================
# 生成器测试
# ========================================
class TestProblemGenerator:
    """问题生成器单元测试"""

    def test_init_empty_operations(self):
        """测试空运算列表初始化"""
        with pytest.raises(ValueError):
            ProblemGenerator([])

    def test_generate_no_duplicates(self):
        """测试生成不重复问题"""
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(100)

        # 检查没有重复
        keys = [p.get_key() for p in problems]
        assert len(keys) == len(set(keys)), "生成的问题应该没有重复"

    def test_generate_count(self):
        """测试生成指定数量"""
        operations = [Addition()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(50)
        assert len(problems) == 50

    def test_generate_zero_count(self):
        """测试生成0个问题"""
        operations = [Addition()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(0)
        assert len(problems) == 0

    def test_generate_negative_count(self):
        """测试生成负数数量"""
        operations = [Addition()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(-10)
        assert len(problems) == 0

    def test_generate_valid_problems(self):
        """测试生成的问题都有效"""
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(50)

        for problem in problems:
            assert 1 <= problem.a <= 99, f"问题 {problem} 的操作数 a 超出范围"
            assert 1 <= problem.b <= 99, f"问题 {problem} 的操作数 b 超出范围"
            if isinstance(problem.operation, Addition):
                assert problem.answer <= 100, f"问题 {problem} 的加法结果超过100"
            elif isinstance(problem.operation, Subtraction):
                assert problem.answer >= 0, f"问题 {problem} 的减法结果为负数"


# ========================================
# 题目集测试
# ========================================
class TestProblemSet:
    """题目集单元测试"""

    @pytest.fixture
    def sample_problems(self):
        """创建示例问题集"""
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        return generator.generate(10)

    @pytest.fixture
    def problem_set(self, sample_problems):
        """创建示例题目集"""
        return ProblemSet(sample_problems)

    def test_count(self, problem_set):
        """测试计数"""
        assert problem_set.count() == 10

    def test_len(self, problem_set):
        """测试len运算符"""
        assert len(problem_set) == 10

    def test_get_problems(self, problem_set):
        """测试获取问题列表"""
        problems = problem_set.get_problems()
        assert len(problems) == 10
        # 测试返回的是副本
        problems.append(None)
        assert problem_set.count() == 10

    def test_getitem(self, problem_set):
        """测试索引访问"""
        assert problem_set[0].a is not None
        assert problem_set[9].a is not None
        with pytest.raises(IndexError):
            _ = problem_set[10]

    def test_count_by_operation(self, problem_set):
        """测试按运算类型计数"""
        total = problem_set.count_by_operation(OperationType.ADDITION) + \
                problem_set.count_by_operation(OperationType.SUBTRACTION)
        assert total == 10

    def test_add_problem(self, problem_set):
        """测试添加问题"""
        initial_count = problem_set.count()
        new_problem = Problem(5, 5, Addition())
        problem_set.add(new_problem)
        assert problem_set.count() == initial_count + 1

    def test_remove_problem(self, problem_set):
        """测试移除问题"""
        initial_count = problem_set.count()
        problem = problem_set[0]
        result = problem_set.remove(problem)
        assert result is True
        assert problem_set.count() == initial_count - 1

    def test_remove_nonexistent_problem(self, problem_set):
        """测试移除不存在的问题"""
        nonexistent = Problem(999, 999, Addition())
        result = problem_set.remove(nonexistent)
        assert result is False

    def test_iteration(self, problem_set):
        """测试原生迭代"""
        count = 0
        for problem in problem_set:
            count += 1
        assert count == 10


# ========================================
# 迭代器测试
# ========================================
class TestProblemIterator:
    """迭代器单元测试"""

    @pytest.fixture
    def sample_problems(self):
        """创建示例问题"""
        return [Problem(i, i, Addition()) for i in range(1, 6)]

    @pytest.fixture
    def iterator(self, sample_problems):
        """创建迭代器"""
        return ProblemIterator(sample_problems)

    def test_has_next_true(self, iterator):
        """测试还有下一个元素"""
        assert iterator.has_next() is True

    def test_has_next_false_after_exhaustion(self, iterator):
        """测试耗尽后没有下一个元素"""
        while iterator.has_next():
            iterator.next()
        assert iterator.has_next() is False

    def test_next(self, iterator):
        """测试获取下一个元素"""
        first = iterator.next()
        assert first is not None

    def test_next_exhausted(self, iterator):
        """测试耗尽后调用next"""
        while iterator.has_next():
            iterator.next()
        with pytest.raises(StopIteration):
            iterator.next()

    def test_reset(self, iterator):
        """测试重置迭代器"""
        # 消耗几个元素
        iterator.next()
        iterator.next()
        iterator.next()

        # 重置
        iterator.reset()
        assert iterator.has_next() is True

    def test_traversal_all_elements(self, iterator):
        """测试遍历所有元素"""
        count = 0
        while iterator.has_next():
            iterator.next()
            count += 1
        assert count == 5


# ========================================
# 格式化器测试
# ========================================
class TestTextFormatter:
    """文本格式化器单元测试"""

    @pytest.fixture
    def formatter(self):
        """创建格式化器"""
        return TextFormatter()

    @pytest.fixture
    def sample_problems(self):
        """创建示例问题"""
        return [Problem(i, i + 1, Addition()) for i in range(5)]

    def test_format_problems(self, formatter, sample_problems):
        """测试格式化题目"""
        result = formatter.format_problems(sample_problems, per_line=2)
        assert "口算练习题" in result
        assert "共 5 道题" in result
        assert "1 + 2 =" in result

    def test_format_answers(self, formatter, sample_problems):
        """测试格式化答案"""
        result = formatter.format_answers(sample_problems, per_line=2)
        assert "参考答案" in result
        assert "1 + 2 = 3" in result

    def test_format_empty_problems(self, formatter):
        """测试格式化空问题集"""
        result = formatter.format_problems([], per_line=5)
        assert "共 0 道题" in result


# ========================================
# 输出器测试
# ========================================
class TestConsoleOutputter:
    """控制台输出器单元测试"""

    @pytest.fixture
    def outputter(self):
        """创建输出器"""
        return ConsoleOutputter()

    def test_output(self, outputter, capsys):
        """测试输出"""
        outputter.output("测试内容")
        captured = capsys.readouterr()
        assert "测试内容" in captured.out


# ========================================
# 打印服务测试
# ========================================
class TestProblemPrintService:
    """打印服务单元测试"""

    @pytest.fixture
    def sample_problems(self):
        """创建示例问题"""
        return [Problem(i, i + 1, Addition()) for i in range(5)]

    @pytest.fixture
    def problem_set(self, sample_problems):
        """创建示例题目集"""
        return ProblemSet(sample_problems)

    @pytest.fixture
    def print_service(self):
        """创建打印服务"""
        formatter = TextFormatter()
        outputter = ConsoleOutputter()
        return ProblemPrintService(formatter, outputter)

    def test_print_problems(self, print_service, problem_set, capsys):
        """测试打印题目"""
        print_service.print_problems(problem_set, per_line=2)
        captured = capsys.readouterr()
        assert "口算练习题" in captured.out

    def test_print_answers(self, print_service, problem_set, capsys):
        """测试打印答案"""
        print_service.print_answers(problem_set, per_line=2)
        captured = capsys.readouterr()
        assert "参考答案" in captured.out


# ========================================
# 工厂模式测试
# ========================================
class TestProblemSetFactory:
    """工厂类单元测试"""

    def test_create_standard_set(self):
        """测试创建标准题目集"""
        problem_set = ProblemSetFactory.create_standard_set()
        assert problem_set.count() == 50
        assert problem_set.count_by_operation(OperationType.ADDITION) > 0
        assert problem_set.count_by_operation(OperationType.SUBTRACTION) > 0

    def test_create_addition_only(self):
        """测试创建仅加法题目集"""
        problem_set = ProblemSetFactory.create_addition_only()
        assert problem_set.count() == 50
        assert problem_set.count_by_operation(OperationType.ADDITION) == 50
        assert problem_set.count_by_operation(OperationType.SUBTRACTION) == 0

    def test_create_subtraction_only(self):
        """测试创建仅减法题目集"""
        problem_set = ProblemSetFactory.create_subtraction_only()
        assert problem_set.count() == 50
        assert problem_set.count_by_operation(OperationType.SUBTRACTION) == 50
        assert problem_set.count_by_operation(OperationType.ADDITION) == 0

    def test_create_custom_count(self):
        """测试创建自定义数量"""
        problem_set = ProblemSetFactory.create_standard_set(30)
        assert problem_set.count() == 30

    def test_create_custom_set(self):
        """测试创建自定义题目集"""
        operations = [Addition()]
        problem_set = ProblemSetFactory.create_custom_set(20, operations)
        assert problem_set.count() == 20

    def test_create_mixed_set(self):
        """测试创建混合运算题目集"""
        problem_set = ProblemSetFactory.create_mixed_set(50, include_multiplication=False)
        assert problem_set.count() == 50
        assert problem_set.count_by_operation(OperationType.MULTIPLICATION) == 0

    def test_create_mixed_set_with_multiplication(self):
        """测试创建包含乘法的混合运算题目集"""
        problem_set = ProblemSetFactory.create_mixed_set(50, include_multiplication=True)
        assert problem_set.count() == 50
        assert problem_set.count_by_operation(OperationType.MULTIPLICATION) > 0


# ========================================
# 策略模式测试
# ========================================
class TestOperationStrategyManager:
    """策略管理器单元测试"""

    @pytest.fixture
    def manager(self):
        """创建策略管理器"""
        return OperationStrategyManager()

    def test_get_available_types(self, manager):
        """测试获取可用策略类型"""
        types = manager.get_available_types()
        assert OperationType.ADDITION in types
        assert OperationType.SUBTRACTION in types
        assert OperationType.MULTIPLICATION in types

    def test_create_strategy_addition(self, manager):
        """测试创建加法策略"""
        strategy = manager.create_strategy(OperationType.ADDITION)
        assert isinstance(strategy, Addition)
        assert strategy.get_symbol() == "+"

    def test_create_strategy_subtraction(self, manager):
        """测试创建减法策略"""
        strategy = manager.create_strategy(OperationType.SUBTRACTION)
        assert isinstance(strategy, Subtraction)
        assert strategy.get_symbol() == "-"

    def test_create_strategy_multiplication(self, manager):
        """测试创建乘法策略"""
        strategy = manager.create_strategy(OperationType.MULTIPLICATION)
        assert isinstance(strategy, Multiplication)
        assert strategy.get_symbol() == "×"

    def test_create_invalid_strategy(self, manager):
        """测试创建无效策略"""
        with pytest.raises(ValueError):
            manager.create_strategy(OperationType.DIVISION)

    def test_register_custom_strategy(self, manager):
        """测试注册自定义策略"""
        # 注意：这只是示例，实际上Division类未定义
        # manager.register(OperationType.DIVISION, Division)
        # strategy = manager.create_strategy(OperationType.DIVISION)
        pass


# ========================================
# 集成测试
# ========================================
class TestIntegration:
    """集成测试 - 测试整个系统的协作"""

    def test_full_workflow(self, capsys):
        """测试完整工作流程"""
        # 1. 创建题目集
        problem_set = ProblemSetFactory.create_standard_set(20)

        # 2. 验证题目数量
        assert problem_set.count() == 20

        # 3. 验证题目有效性
        for problem in problem_set:
            assert 1 <= problem.a <= 99
            assert 1 <= problem.b <= 99
            if isinstance(problem.operation, Addition):
                assert problem.answer <= 100
            elif isinstance(problem.operation, Subtraction):
                assert problem.answer >= 0

        # 4. 验证没有重复
        keys = [p.get_key() for p in problem_set]
        assert len(keys) == len(set(keys))

        # 5. 打印题目
        formatter = TextFormatter()
        outputter = ConsoleOutputter()
        print_service = ProblemPrintService(formatter, outputter)
        print_service.print_problems(problem_set, per_line=5)
        captured = capsys.readouterr()
        assert "口算练习题" in captured.out

    def test_iterator_with_generator(self):
        """测试迭代器与生成器集成"""
        problem_set = ProblemSetFactory.create_standard_set(10)
        iterator = problem_set.create_iterator()

        count = 0
        while iterator.has_next():
            problem = iterator.next()
            assert isinstance(problem, Problem)
            count += 1

        assert count == 10

    def test_strategy_with_generator(self):
        """测试策略与生成器集成"""
        manager = OperationStrategyManager()
        operations = [
            manager.create_strategy(OperationType.ADDITION),
            manager.create_strategy(OperationType.SUBTRACTION),
        ]
        generator = ProblemGenerator(operations)
        problems = generator.generate(10)

        assert len(problems) == 10


# ========================================
# 边界条件测试
# ========================================
class TestEdgeCases:
    """边界条件测试"""

    def test_maximum_sum(self):
        """测试最大和"""
        addition = Addition()
        problem = Problem(50, 50, addition)
        assert problem.answer == 100

    def test_minimum_sum(self):
        """测试最小和"""
        addition = Addition()
        problem = Problem(1, 1, addition)
        assert problem.answer == 2

    def test_maximum_difference(self):
        """测试最大差"""
        subtraction = Subtraction()
        problem = Problem(99, 1, subtraction)
        assert problem.answer == 98

    def test_minimum_difference(self):
        """测试最小差"""
        subtraction = Subtraction()
        problem = Problem(10, 10, subtraction)
        assert problem.answer == 0

    def test_large_generation_count(self):
        """测试大数量生成"""
        operations = [Addition(), Subtraction()]
        generator = ProblemGenerator(operations)
        problems = generator.generate(200)
        # 可能无法生成200道不重复的题目，但要能正常运行
        assert len(problems) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])