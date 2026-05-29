# 口算练习题生成器

一个基于面向对象设计原则的口算练习题生成系统，用于生成小学数学口算练习题。

## 项目特性

- ✅ 面向对象设计，严格遵循SOLID原则
- ✅ 应用多种设计模式（策略模式、工厂模式、迭代器模式、门面模式）
- ✅ 完整的单元测试覆盖
- ✅ 支持多种运算类型（加法、减法、乘法）
- ✅ 自动去重，确保题目不重复
- ✅ 灵活的配置和扩展

## 核心设计原则

### 1. 面向对象核心概念
- **抽象**: 通过抽象基类 `IOperation` 定义运算接口
- **封装**: 类封装数据和行为，隐藏内部实现细节
- **多态**: 不同运算类型统一处理，运行时动态选择
- **继承**: 具体运算类继承抽象基类，复用代码

### 2. SOLID原则
- **SRP (单一职责)**: 每个类只负责一件事
- **OCP (开放封闭)**: 对扩展开放，对修改封闭
- **LSP (里氏代换)**: 子类可以替换基类
- **ISP (接口隔离)**: 接口精简，客户端只依赖需要的接口
- **DIP (依赖倒转)**: 依赖抽象而非具体实现

### 3. 设计模式应用

| 设计模式 | 应用位置 | 用途 |
|---------|---------|------|
| 策略模式 | `IOperation` 及其实现类 | 运行时选择不同的运算策略 |
| 工厂模式 | `ProblemSetFactory` | 集中管理问题集的创建 |
| 迭代器模式 | `ProblemIterator` | 提供对问题集的统一遍历 |
| 模板方法模式 | `BaseOperation` | 定义运算算法骨架 |
| 门面模式 | `ProblemPrintService` | 简化格式化和输出调用 |

## 项目结构

```
.
├── math_problem_generator.py      # 主程序文件
├── test_math_problem_generator.py # 单元测试文件
├── UML_CLASS_DIAGRAM.md           # UML类图设计文档
├── README.md                      # 项目说明文档
└── .gitignore                     # Git忽略文件配置
```

## 类结构概览

```
IOperation (接口)
    ↑
    ├── Addition (加法运算)
    ├── Subtraction (减法运算)
    └── Multiplication (乘法运算)

Problem (算式问题)
    ↓
ProblemSet (问题集)
    ↓
ProblemIterator (迭代器)

ProblemSetFactory (工厂)
    ↓
ProblemGenerator (生成器)
    ↓
ProblemPrintService (打印服务)
```

## 安装要求

- Python 3.8+
- pytest (用于运行单元测试)

## 安装依赖

```bash
pip install pytest
```

## 运行程序

```bash
python math_problem_generator.py
```

## 运行单元测试

```bash
# 运行所有测试
pytest test_math_problem_generator.py -v

# 运行特定测试类
pytest test_math_problem_generator.py::TestAddition -v

# 运行特定测试方法
pytest test_math_problem_generator.py::TestAddition::test_calculate_valid_cases -v

# 生成覆盖率报告
pytest test_math_problem_generator.py --cov=. --cov-report=html
```

## 使用示例

### 基础使用

```python
from math_problem_generator import ProblemSetFactory, ProblemPrintService, TextFormatter, ConsoleOutputter

# 创建标准题目集（50题，加减法混合）
problem_set = ProblemSetFactory.create_standard_set()

# 打印题目和答案
formatter = TextFormatter()
outputter = ConsoleOutputter()
print_service = ProblemPrintService(formatter, outputter)

print_service.print_problems(problem_set, per_line=5)
print_service.print_answers(problem_set, per_line=5)
```

### 自定义配置

```python
from math_problem_generator import (
    ProblemSetFactory,
    ProblemGenerator,
    Addition,
    Subtraction,
    ProblemSet,
    ProblemPrintService,
    TextFormatter,
    ConsoleOutputter
)

# 创建仅加法的题目集
addition_set = ProblemSetFactory.create_addition_only(count=30)

# 创建仅减法的题目集
subtraction_set = ProblemSetFactory.create_subtraction_only(count=30)

# 创建混合运算题目集（包含乘法）
mixed_set = ProblemSetFactory.create_mixed_set(count=50, include_multiplication=True)

# 创建完全自定义的题目集
operations = [Addition(), Subtraction()]
generator = ProblemGenerator(operations)
problems = generator.generate(50)
custom_set = ProblemSet(problems)
```

### 使用策略管理器

```python
from math_problem_generator import OperationStrategyManager, OperationType

# 创建策略管理器
manager = OperationStrategyManager()

# 获取可用策略类型
types = manager.get_available_types()
print(f"可用运算类型: {[t.name for t in types]}")

# 创建策略实例
addition_strategy = manager.create_strategy(OperationType.ADDITION)
subtraction_strategy = manager.create_strategy(OperationType.SUBTRACTION)
```

### 使用迭代器

```python
from math_problem_generator import ProblemSetFactory

problem_set = ProblemSetFactory.create_standard_set()

# 使用自定义迭代器
iterator = problem_set.create_iterator()
while iterator.has_next():
    problem = iterator.next()
    print(f"题目: {problem.with_answer()}")

# 使用Python原生迭代
for problem in problem_set:
    print(f"题目: {problem.with_answer()}")
```

### 统计信息

```python
from math_problem_generator import ProblemSetFactory, OperationType

problem_set = ProblemSetFactory.create_standard_set()

print(f"总题数: {problem_set.count()}")
print(f"加法题数: {problem_set.count_by_operation(OperationType.ADDITION)}")
print(f"减法题数: {problem_set.count_by_operation(OperationType.SUBTRACTION)}")
```

## 扩展示例

### 添加新的运算类型

```python
from math_problem_generator import BaseOperation, OperationType, OperationConfig

class Division(BaseOperation):
    """除法运算"""

    def __init__(self):
        config = OperationConfig(OperationType.DIVISION, max_value=81, max_result=9)
        super().__init__(config)

    def calculate(self, a: int, b: int) -> int:
        return a // b  # 整除

    def is_valid(self, a: int, b: int) -> bool:
        if b == 0:
            return False
        result = self.calculate(a, b)
        return result >= 0 and a % b == 0  # 确保能整除

    def get_symbol(self) -> str:
        return "÷"

    def get_operation_type(self) -> OperationType:
        return OperationType.DIVISION

# 使用新的运算类型
from math_problem_generator import ProblemSetFactory
operations = [Division()]
division_set = ProblemSetFactory.create_custom_set(50, operations)
```

### 自定义格式化器

```python
from math_problem_generator import IFormatter, List

class HTMLFormatter:
    """HTML格式化器"""

    def format_problems(self, problems: List, per_line: int = 5) -> str:
        html = ["<html><body><h1>口算练习题</h1><table>"]
        for i, problem in enumerate(problems, 1):
            if (i - 1) % per_line == 0:
                html.append("<tr>")
            html.append(f"<td>{problem.with_answer()}</td>")
            if i % per_line == 0:
                html.append("</tr>")
        html.append("</table></body></html>")
        return "\n".join(html)

    def format_answers(self, problems: List, per_line: int = 5) -> str:
        # 实现答案格式化
        pass
```

### 自定义输出器

```python
from math_problem_generator import IOutputter

class FileOutputter:
    """文件输出器"""

    def __init__(self, filename: str):
        self.filename = filename

    def output(self, content: str) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(content)

# 使用文件输出器
from math_problem_generator import ProblemPrintService, TextFormatter
formatter = TextFormatter()
outputter = FileOutputter("practice_problems.txt")
print_service = ProblemPrintService(formatter, outputter)
print_service.print_problems(problem_set)
```

## 测试覆盖率

项目包含完整的单元测试，覆盖以下方面：

- ✅ 运算类的功能测试
- ✅ 问题类的功能测试
- ✅ 生成器的功能测试
- ✅ 题目集的功能测试
- ✅ 格式化器的功能测试
- ✅ 工厂模式测试
- ✅ 策略模式测试
- ✅ 迭代器模式测试
- ✅ 集成测试
- ✅ 边界条件测试

## 编码规范

项目遵循以下编码规范：

1. **命名规范**
   - 类名使用大驼峰命名法（PascalCase）
   - 函数和变量名使用小写下划线命名法（snake_case）
   - 私有成员使用单下划线前缀
   - 常量使用大写下划线命名法

2. **类型注解**
   - 所有函数都添加类型注解
   - 使用 `typing` 模块的类型

3. **文档字符串**
   - 所有类和公开方法都有文档字符串
   - 使用Google风格的文档字符串

4. **代码组织**
   - 相关功能组织在一起
   - 使用清晰的注释分隔不同模块

## Git工作流

### 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例：**

```
feat(operation): add multiplication operation

Implement multiplication operation class following the strategy pattern.
- Add Multiplication class inheriting from BaseOperation
- Update OperationStrategyManager to include multiplication
- Add unit tests for multiplication operation

Closes #5
```

### 分支策略

- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支
- `hotfix/*`: 紧急修复分支

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目仅用于教学和学习目的。

## 作者

面向对象软件构造课程示例

## 致谢

感谢本项目的所有贡献者。

---

**注**: 本项目是面向对象软件构造课程的示例，展示如何应用面向对象设计原则和设计模式。