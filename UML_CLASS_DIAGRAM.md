# UML类图设计文档

## 口算练习题生成器 - 类图

本系统采用面向对象设计，遵循SOLID原则，应用多种设计模式。

```mermaid
classDiagram
    %% 抽象数据类型
    class OperationType {
        <<enumeration>>
        ADDITION
        SUBTRACTION
        MULTIPLICATION
        DIVISION
    }

    class OperationConfig {
        +operation_type: OperationType
        +min_value: int
        +max_value: int
        +max_result: int
        +min_result: int
    }

    %% 抽象接口/协议
    class IOperation {
        <<interface>>
        +calculate(a: int, b: int) int
        +is_valid(a: int, b: int) bool
        +get_symbol() str
        +get_operation_type() OperationType
        +get_comparison_key(a: int, b: int) tuple
    }

    class IFormatter {
        <<interface>>
        +format_problems(problems: List~Problem~, per_line: int) str
        +format_answers(problems: List~Problem~, per_line: int) str
    }

    class IOutputter {
        <<interface>>
        +output(content: str) None
    }

    class IIterator {
        <<interface>>
        +has_next() bool
        +next() Problem
    }

    class IAggregate {
        <<interface>>
        +create_iterator() IIterator
    }

    %% 抽象基类
    class BaseOperation {
        <<abstract>>
        #config: OperationConfig
        +get_comparison_key(a: int, b: int) tuple
        +get_symbol() str
    }

    %% 具体运算类（策略模式 - 具体策略）
    class Addition {
        -config: OperationConfig
        +calculate(a: int, b: int) int
        +is_valid(a: int, b: int) bool
        +get_symbol() str
        +get_operation_type() OperationType
        +get_comparison_key(a: int, b: int) tuple
    }

    class Subtraction {
        -config: OperationConfig
        +calculate(a: int, b: int) int
        +is_valid(a: int, b: int) bool
        +get_symbol() str
        +get_operation_type() OperationType
        +get_comparison_key(a: int, b: int) tuple
    }

    class Multiplication {
        -config: OperationConfig
        +calculate(a: int, b: int) int
        +is_valid(a: int, b: int) bool
        +get_symbol() str
        +get_operation_type() OperationType
    }

    %% 实体类
    class Problem {
        -_a: int
        -_b: int
        -_operation: IOperation
        -_answer: int
        +Problem(a: int, b: int, operation: IOperation)
        +a: int
        +b: int
        +operation: IOperation
        +answer: int
        +__str__() str
        +with_answer() str
        +get_key() tuple
        +equals(other: Problem) bool
    }

    %% 生成器类
    class ProblemGenerator {
        -_operations: List~IOperation~
        +ProblemGenerator(operations: List~IOperation~)
        +generate(count: int) List~Problem~
        -_generate_single() Problem
    }

    %% 迭代器类（迭代器模式）
    class ProblemIterator {
        -_problems: List~Problem~
        -_position: int
        +ProblemIterator(problems: List~Problem~)
        +has_next() bool
        +next() Problem
        +reset() None
    }

    %% 题目集类（聚合类）
    class ProblemSet {
        -_problems: List~Problem~
        +ProblemSet(problems: List~Problem~)
        +create_iterator() ProblemIterator
        +get_problems() List~Problem~
        +count() int
        +count_by_operation(operation_type: OperationType) int
        +add(problem: Problem) None
        +remove(problem: Problem) bool
        +__len__() int
        +__getitem__(index: int) Problem
    }

    %% 格式化器类
    class TextFormatter {
        +format_problems(problems: List~Problem~, per_line: int) str
        +format_answers(problems: List~Problem~, per_line: int) str
    }

    %% 输出器类
    class ConsoleOutputter {
        +output(content: str) None
    }

    %% 打印服务（门面模式）
    class ProblemPrintService {
        -_formatter: IFormatter
        -_outputter: IOutputter
        +ProblemPrintService(formatter: IFormatter, outputter: IOutputter)
        +print_problems(problem_set: ProblemSet, per_line: int) None
        +print_answers(problem_set: ProblemSet, per_line: int) None
    }

    %% 工厂类（工厂模式）
    class ProblemSetFactory {
        <<static>>
        +create_standard_set(count: int) ProblemSet
        +create_addition_only(count: int) ProblemSet
        +create_subtraction_only(count: int) ProblemSet
        +create_multiplication_set(count: int) ProblemSet
        +create_custom_set(count: int, operations: List~IOperation~) ProblemSet
        +create_mixed_set(count: int, include_multiplication: bool) ProblemSet
    }

    %% 策略管理器（策略模式 - 上下文类）
    class OperationStrategyManager {
        -_strategies: Dict~OperationType, type~
        +OperationStrategyManager()
        +register(operation_type: OperationType, strategy_class: type) None
        +create_strategy(operation_type: OperationType) IOperation
        +get_available_types() List~OperationType~
        -_register_default_strategies() None
    }

    %% 关系定义
    IOperation <|.. BaseOperation : 实现
    BaseOperation <|-- Addition : 继承
    BaseOperation <|-- Subtraction : 继承
    BaseOperation <|-- Multiplication : 继承

    IOperation <|.. Addition : 实现
    IOperation <|.. Subtraction : 实现
    IOperation <|.. Multiplication : 实现

    Problem *-- IOperation : 依赖
    ProblemSet o-- Problem : 聚合

    ProblemGenerator o-- IOperation : 依赖

    ProblemSet ..|> IAggregate : 实现
    ProblemSet --> ProblemIterator : 创建
    ProblemIterator ..|> IIterator : 实现

    IFormatter <|.. TextFormatter : 实现
    IOutputter <|.. ConsoleOutputter : 实现

    ProblemPrintService *-- IFormatter : 依赖
    ProblemPrintService *-- IOutputter : 依赖
    ProblemPrintService --> ProblemSet : 使用

    ProblemSetFactory ..> ProblemGenerator : 使用
    ProblemSetFactory ..> ProblemSet : 创建

    OperationStrategyManager --> IOperation : 创建
    OperationStrategyManager --> Addition : 使用
    OperationStrategyManager --> Subtraction : 使用
    OperationStrategyManager --> Multiplication : 使用

    Addition *-- OperationConfig : 依赖
    Subtraction *-- OperationConfig : 依赖
    Multiplication *-- OperationConfig : 依赖
```

## 类关系说明

### 1. 继承关系 (Inheritance)
- `BaseOperation` 作为抽象基类，定义运算的通用行为
- `Addition`, `Subtraction`, `Multiplication` 继承自 `BaseOperation`
- 应用**模板方法模式**，基类提供默认实现，子类可重写

### 2. 实现关系 (Implementation)
- `IOperation` 是运算接口（Python中用Protocol模拟）
- `Addition`, `Subtraction`, `Multiplication` 实现 `IOperation` 接口
- 应用**策略模式**，不同运算作为不同的策略

### 3. 依赖关系 (Dependency)
- `Problem` 依赖 `IOperation` 接口，而非具体实现（依赖倒转原则）
- `ProblemGenerator` 依赖 `IOperation` 列表
- `ProblemPrintService` 依赖 `IFormatter` 和 `IOutputter` 接口

### 4. 聚合关系 (Aggregation)
- `ProblemSet` 聚合多个 `Problem` 对象
- `ProblemSet` 可以独立于 `Problem` 存在

### 5. 组合关系 (Composition)
- `Problem` 组合 `IOperation` 对象
- `Problem` 不存在时，`IOperation` 对象也可能被释放

## 设计模式应用

### 1. 策略模式 (Strategy Pattern)
- **接口**: `IOperation`
- **具体策略**: `Addition`, `Subtraction`, `Multiplication`
- **上下文**: `OperationStrategyManager`
- **用途**: 运行时选择不同的运算策略

### 2. 工厂模式 (Factory Pattern)
- **工厂类**: `ProblemSetFactory`
- **产品**: `ProblemSet`
- **用途**: 集中管理问题集的创建逻辑

### 3. 迭代器模式 (Iterator Pattern)
- **迭代器接口**: `IIterator`
- **具体迭代器**: `ProblemIterator`
- **聚合接口**: `IAggregate`
- **具体聚合**: `ProblemSet`
- **用途**: 提供对问题集的统一遍历方式

### 4. 模板方法模式 (Template Method Pattern)
- **抽象类**: `BaseOperation`
- **具体类**: `Addition`, `Subtraction`, `Multiplication`
- **用途**: 定义算法骨架，子类实现具体步骤

### 5. 门面模式 (Facade Pattern)
- **门面**: `ProblemPrintService`
- **子系统**: `TextFormatter`, `ConsoleOutputter`
- **用途**: 简化格式化和输出的复杂调用

## SOLID原则体现

### 单一职责原则 (SRP)
- `Problem`: 只负责表示一道算式
- `ProblemGenerator`: 只负责生成问题
- `ProblemSet`: 只负责管理问题集
- `TextFormatter`: 只负责格式化
- `ConsoleOutputter`: 只负责输出

### 开放封闭原则 (OCP)
- 通过 `IOperation` 接口，可以轻松添加新的运算类型（如乘法、除法）
- 通过 `IFormatter` 接口，可以添加新的格式化器（如HTML、PDF）
- 通过 `IOutputter` 接口，可以添加新的输出方式（如文件、网络）

### 里氏代换原则 (LSP)
- `Addition`, `Subtraction`, `Multiplication` 都可以替换 `IOperation`
- 迭代器可以替换 `IIterator`

### 接口隔离原则 (ISP)
- `IOperation`: 只包含运算相关的操作
- `IFormatter`: 只包含格式化相关的操作
- `IOutputter`: 只包含输出相关的操作
- `IIterator`: 只包含迭代相关的操作

### 依赖倒转原则 (DIP)
- `Problem` 依赖 `IOperation` 抽象，而非具体运算类
- `ProblemGenerator` 依赖 `IOperation` 抽象
- `ProblemPrintService` 依赖 `IFormatter` 和 `IOutputter` 抽象

## 抽象数据类型 (ADT)

### OperationType
- 枚举类型，表示不同的运算类型
- 类型安全的运算标识

### OperationConfig
- 数据类，封装运算配置
- 作为运算策略的参数传递

### Problem
- 封装算式的完整信息
- 提供只读属性，保证不可变性
- 自我封装计算逻辑

## 多态性应用

### 运行时多态
- `ProblemGenerator` 可以处理任何实现 `IOperation` 的策略
- `ProblemPrintService` 可以使用任何 `IFormatter` 和 `IOutputter`

### 参数化多态
- `ProblemSet` 可以存储任何 `Problem` 对象
- 泛型接口支持不同类型的数据处理