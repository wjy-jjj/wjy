# 编程规范文档

## Python编码规范 (PEP 8)

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | 大驼峰 (PascalCase) | `class ProblemSet:` |
| 函数名 | 小写下划线 (snake_case) | `def calculate_sum():` |
| 变量名 | 小写下划线 (snake_case) | `problem_count = 10` |
| 常量 | 大写下划线 (UPPER_SNAKE) | `MAX_COUNT = 100` |
| 私有成员 | 单下划线前缀 | `def _helper():` |
| 私有类成员 | 双下划线前缀 | `def __private_method():` |

### 缩进和空格

```python
# 使用4个空格缩进
class Problem:
    def calculate(self):
        result = self.a + self.b
        return result

# 运算符两边加空格
result = a + b  # 正确
result = a+b     # 错误

# 函数参数逗号后加空格
def func(a, b, c):
    pass

# 列表、字典元素逗号后加空格
items = [1, 2, 3]
mapping = {'key': 'value'}
```

### 导入顺序

```python
# 1. 标准库导入
import os
import sys
from abc import ABC, abstractmethod

# 2. 第三方库导入
import pytest

# 3. 本地模块导入
from my_module import MyClass
```

## 类型注解

### 函数签名

```python
from typing import List, Optional, Dict

def generate_problems(count: int, operations: List[IOperation]) -> List[Problem]:
    """生成指定数量的题目

    Args:
        count: 要生成的题目数量
        operations: 可用的运算类型列表

    Returns:
        生成的题目列表
    """
    pass

def find_problem(problems: List[Problem], answer: int) -> Optional[Problem]:
    """查找指定答案的问题

    Args:
        problems: 问题列表
        answer: 要查找的答案

    Returns:
        找到的问题，未找到返回None
    """
    pass
```

### 类属性注解

```python
class ProblemSet:
    def __init__(self, problems: List[Problem]) -> None:
        self._problems: List[Problem] = problems
        self._count: int = len(problems)

    def count(self) -> int:
        return self._count
```

## 文档字符串

### Google风格

```python
def calculate(a: int, b: int, operation: str) -> int:
    """执行四则运算。

    根据指定的运算符对两个数进行计算。

    Args:
        a: 第一个操作数
        b: 第二个操作数
        operation: 运算符，可以是 +、-、*、/

    Returns:
        计算结果

    Raises:
        ValueError: 当运算符无效时
        ZeroDivisionError: 当除数为0时

    Examples:
        >>> calculate(10, 5, '+')
        15
        >>> calculate(10, 5, '/')
        2
    """
    pass
```

### 类文档字符串

```python
class ProblemGenerator:
    """问题生成器 - 生成不重复的算式

    负责根据指定的运算类型和数量生成口算题目。
    确保生成的题目不重复，并满足业务规则。

    Attributes:
        _operations: 可用的运算类型列表

    Examples:
        >>> operations = [Addition(), Subtraction()]
        >>> generator = ProblemGenerator(operations)
        >>> problems = generator.generate(50)
        >>> len(problems)
        50
    """

    def __init__(self, operations: List[IOperation]):
        """初始化问题生成器

        Args:
            operations: 可用的运算类型列表，至少包含一个运算

        Raises:
            ValueError: 当运算列表为空时
        """
        pass
```

## 代码组织

### 文件结构

```python
# 1. 文件头注释
"""
模块描述
作者信息
许可证信息
"""

# 2. 标准库导入
import os
import sys

# 3. 第三方库导入
import pytest

# 4. 本地模块导入
from . import helper

# 5. 模块常量
MAX_COUNT = 100
DEFAULT_COUNT = 50

# 6. 异常类定义
class CustomError(Exception):
    pass

# 7. 接口/抽象类定义
class IInterface(Protocol):
    pass

# 8. 类定义
class MyClass:
    pass

# 9. 函数定义
def main():
    pass

# 10. 主程序入口
if __name__ == "__main__":
    main()
```

### 类组织

```python
class MyClass:
    """类文档字符串"""

    # 1. 类属性
    CLASS_ATTRIBUTE = "value"

    # 2. __init__ 方法
    def __init__(self):
        pass

    # 3. 魔术方法
    def __str__(self):
        pass

    def __repr__(self):
        pass

    # 4. 公开方法
    def public_method(self):
        pass

    # 5. 属性访问器
    @property
    def my_property(self):
        pass

    # 6. 私有方法
    def _private_method(self):
        pass
```

## 错误处理

### 异常处理

```python
# 明确的异常类型
try:
    result = divide(a, b)
except ZeroDivisionError:
    logger.error("除数不能为零")
    return 0
except ValueError as e:
    logger.error(f"数值错误: {e}")
    raise
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise

# 自定义异常
class InvalidOperationError(Exception):
    """无效运算异常"""
    pass

# 使用自定义异常
if operation not in ['+', '-', '*', '/']:
    raise InvalidOperationError(f"不支持的运算符: {operation}")
```

## 注释规范

### 行内注释

```python
# 计算结果
result = a + b

# 确保数量不超过限制
if count > MAX_COUNT:
    count = MAX_COUNT  # 截断到最大值
```

### 块注释

```python
# ========================================
# 这是一个重要的代码块
# 功能说明
# ========================================
def important_function():
    pass
```

### TODO注释

```python
# TODO: 添加对乘法运算的支持
# FIXME: 这个方法可能有性能问题
# NOTE: 这个方法假设输入已经验证
```

## 测试规范

### 测试命名

```python
class TestProblemGenerator:
    """问题生成器测试类"""

    def test_generate_with_valid_count(self):
        """测试生成指定数量的题目"""
        pass

    def test_generate_with_zero_count(self):
        """测试生成0个题目"""
        pass

    def test_generate_with_negative_count(self):
        """测试生成负数数量的题目"""
        pass
```

### 测试结构

```python
import pytest

class TestAddition:
    """加法运算测试"""

    @pytest.fixture
    def addition(self):
        """测试夹具 - 创建加法实例"""
        return Addition()

    def test_calculate_with_valid_numbers(self, addition):
        """测试有效数字的计算"""
        result = addition.calculate(10, 20)
        assert result == 30

    def test_calculate_with_edge_cases(self, addition):
        """测试边界情况"""
        assert addition.calculate(50, 50) == 100  # 最大和
        assert addition.calculate(1, 1) == 2      # 最小和
```

## Git提交规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

| 类型 | 描述 | 示例 |
|------|------|------|
| feat | 新功能 | feat(operation): add multiplication operation |
| fix | 修复bug | fix(generator): fix duplicate problem generation |
| docs | 文档更新 | docs: update README with new features |
| style | 代码格式 | style: format code with black |
| refactor | 重构 | refactor(problem): simplify get_key method |
| test | 测试相关 | test(addition): add edge case tests |
| chore | 构建/工具 | chore: update pytest version |

### 提交示例

```
feat(generator): add problem count validation

Validate the count parameter to ensure it's non-negative.
Raise ValueError if negative count is provided.

- Add validation in generate() method
- Add unit tests for invalid count
- Update documentation

Closes #12

Co-authored-by: John Doe <john@example.com>
```

## 代码审查检查清单

### 功能性
- [ ] 代码是否实现了预期功能
- [ ] 边界条件是否处理正确
- [ ] 错误处理是否完善
- [ ] 是否有潜在的bug

### 可读性
- [ ] 变量和函数命名是否清晰
- [ ] 是否有必要的注释
- [ ] 代码结构是否清晰
- [ ] 是否符合团队编码规范

### 性能
- [ ] 是否有性能问题
- [ ] 算法复杂度是否合理
- [ ] 是否有内存泄漏风险

### 安全性
- [ ] 是否有安全漏洞
- [ ] 输入是否正确验证
- [ ] 敏感数据是否正确处理

### 测试
- [ ] 是否有单元测试
- [ ] 测试覆盖率是否足够
- [ ] 测试是否通过

### 文档
- [ ] 是否更新了相关文档
- [ ] API文档是否完整
- [ ] README是否更新

## 最佳实践

### 面向对象设计

```python
# 使用依赖注入
class ProblemPrinter:
    def __init__(self, formatter: IFormatter, outputter: IOutputter):
        self._formatter = formatter
        self._outputter = outputter

# 优于
class ProblemPrinter:
    def __init__(self):
        self._formatter = TextFormatter()  # 硬编码依赖
```

### 不可变性

```python
# 使用属性而非直接访问
class Problem:
    def __init__(self, a: int, b: int):
        self._a = a
        self._b = b

    @property
    def a(self) -> int:
        return self._a  # 只读，不能修改

# 优于
class Problem:
    def __init__(self, a: int, b: int):
        self.a = a  # 可以被意外修改
        self.b = b
```

### 接口隔离

```python
# 定义多个小接口
class IReadable(Protocol):
    def read(self) -> str: ...

class IWritable(Protocol):
    def write(self, content: str) -> None: ...

# 而非一个大接口
class IStorage(Protocol):
    def read(self) -> str: ...
    def write(self, content: str) -> None: ...
    def delete(self) -> bool: ...
    # ... 更多方法
```

## 工具配置

### .editorconfig

```ini
root = true

[*.py]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### pyproject.toml (代码格式化)

```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88
```

### pyproject.toml (代码检查)

```toml
[tool.pylint.messages_control]
disable = [
    "C0111",  # missing-docstring
    "C0103",  # invalid-name
]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## 资源链接

- [PEP 8 - Python代码风格指南](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 - 文档字符串约定](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - 类型注解](https://www.python.org/dev/peps/pep-0484/)
- [Google Python风格指南](https://google.github.io/styleguide/pyguide.html)
- [Git提交信息规范](https://www.conventionalcommits.org/)