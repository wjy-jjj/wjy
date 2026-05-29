"""
口算练习系统 - 主程序入口
集成所有功能，提供CLI菜单导航

菜单功能：
1. 生成标准练习题（50道，加减法混合）
2. 生成加法练习题
3. 生成减法练习题
4. 生成乘法练习题
5. 生成混合练习题
6. 交互练习（小明使用）
7. 退出系统
"""

from typing import Optional

from src.core import (
    ProblemSetFactory,
    ProblemPrintService,
    TextFormatter,
    ConsoleOutputter,
    ProblemSet,
    Problem,
)


class InteractivePractice:
    """交互练习模块 - 支持实时练习和批改"""

    def __init__(self, problem_set: ProblemSet):
        self._problem_set = problem_set
        self._correct_count = 0
        self._wrong_count = 0
        self._wrong_problems = []

    def start(self) -> None:
        """开始交互练习"""
        print("\n" + "=" * 60)
        print("          交 互 练 习 模 式")
        print("=" * 60)
        print(f"本次练习共 {self._problem_set.count()} 道题")
        print("请输入每题的答案，按回车键确认")
        print("输入 'q' 或 'Q' 可随时退出练习")
        print("-" * 60)

        for index, problem in enumerate(self._problem_set.get_problems(), 1):
            user_answer = self._get_user_input(problem, index)
            
            if user_answer is None:
                print("\n练习已退出")
                break
            
            self._check_answer(problem, user_answer)

        self._show_summary()

    def _get_user_input(self, problem: Problem, index: int) -> Optional[int]:
        """获取用户输入"""
        while True:
            try:
                user_input = input(f"[{index}] {problem}").strip()
                
                if user_input.lower() == 'q':
                    return None
                
                if not user_input:
                    print("请输入答案")
                    continue
                
                return int(user_input)
            except ValueError:
                print("请输入有效的数字")

    def _check_answer(self, problem: Problem, user_answer: int) -> None:
        """检查答案并反馈"""
        if user_answer == problem.answer:
            print(f"  ✓ 正确！答案是 {problem.answer}")
            self._correct_count += 1
        else:
            print(f"  ✗ 错误！正确答案是 {problem.answer}")
            self._wrong_count += 1
            self._wrong_problems.append(problem)

    def _show_summary(self) -> None:
        """显示练习总结"""
        print("\n" + "=" * 60)
        print("          练 习 结 束")
        print("=" * 60)
        total = self._correct_count + self._wrong_count
        print(f"完成题数: {total} 道")
        print(f"正确题数: {self._correct_count} 道")
        print(f"错误题数: {self._wrong_count} 道")
        
        if total > 0:
            accuracy = (self._correct_count / total) * 100
            print(f"正确率: {accuracy:.1f}%")
            
            if accuracy >= 90:
                print("🎉 太棒了！继续保持！")
            elif accuracy >= 70:
                print("👍 不错！继续努力！")
            elif accuracy >= 60:
                print("💪 需要多加练习！")
            else:
                print("📚 加油！多做练习会更好！")

        if self._wrong_problems:
            print("\n--- 错题回顾 ---")
            formatter = TextFormatter()
            print(formatter.format_answers(self._wrong_problems, per_line=3))


class MenuSystem:
    """菜单系统 - CLI导航"""

    def __init__(self):
        self._current_problem_set: Optional[ProblemSet] = None
        self._formatter = TextFormatter()
        self._outputter = ConsoleOutputter()
        self._print_service = ProblemPrintService(self._formatter, self._outputter)

    def run(self) -> None:
        """运行菜单系统"""
        self._show_welcome()
        
        while True:
            self._show_main_menu()
            choice = self._get_menu_choice(1, 7)
            
            if choice == 1:
                self._generate_standard_set()
            elif choice == 2:
                self._generate_addition_set()
            elif choice == 3:
                self._generate_subtraction_set()
            elif choice == 4:
                self._generate_multiplication_set()
            elif choice == 5:
                self._generate_mixed_set()
            elif choice == 6:
                self._start_interactive_practice()
            elif choice == 7:
                self._exit_system()
                break

    def _show_welcome(self) -> None:
        """显示欢迎信息"""
        print("")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                    口算练习系统 v3.0                           ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print("║  专为小学生设计的数学口算练习工具                              ║")
        print("║  支持加法、减法、乘法运算练习                                  ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print("")

    def _show_main_menu(self) -> None:
        """显示主菜单"""
        print("=" * 60)
        print("                        主 菜 单")
        print("=" * 60)
        print(" 1. 生成标准练习题（加减法混合，50道）")
        print(" 2. 生成加法练习题")
        print(" 3. 生成减法练习题")
        print(" 4. 生成乘法练习题")
        print(" 5. 生成混合练习题（含乘法）")
        print(" 6. 交互练习模式（小明专用）")
        print(" 7. 退出系统")
        print("=" * 60)

    def _get_menu_choice(self, min_choice: int, max_choice: int) -> int:
        """获取菜单选择"""
        while True:
            try:
                choice = int(input("请输入选择 (1-7): ").strip())
                if min_choice <= choice <= max_choice:
                    return choice
                print(f"请输入有效的数字 ({min_choice}-{max_choice})")
            except ValueError:
                print("请输入有效的数字")

    def _get_problem_count(self) -> int:
        """获取题目数量"""
        while True:
            try:
                count = int(input("请输入题目数量: ").strip())
                if 1 <= count <= 200:
                    return count
                print("请输入1-200之间的数字")
            except ValueError:
                print("请输入有效的数字")

    def _generate_standard_set(self) -> None:
        """生成标准练习题"""
        count = self._get_problem_count()
        self._current_problem_set = ProblemSetFactory.create_standard_set(count)
        self._display_problems()

    def _generate_addition_set(self) -> None:
        """生成加法练习题"""
        count = self._get_problem_count()
        self._current_problem_set = ProblemSetFactory.create_addition_only(count)
        self._display_problems()

    def _generate_subtraction_set(self) -> None:
        """生成减法练习题"""
        count = self._get_problem_count()
        self._current_problem_set = ProblemSetFactory.create_subtraction_only(count)
        self._display_problems()

    def _generate_multiplication_set(self) -> None:
        """生成乘法练习题"""
        count = self._get_problem_count()
        self._current_problem_set = ProblemSetFactory.create_multiplication_set(count)
        self._display_problems()

    def _generate_mixed_set(self) -> None:
        """生成混合练习题"""
        count = self._get_problem_count()
        self._current_problem_set = ProblemSetFactory.create_mixed_set(count, include_multiplication=True)
        self._display_problems()

    def _display_problems(self) -> None:
        """显示生成的题目"""
        if self._current_problem_set:
            print("\n--- 练习题 ---")
            self._print_service.print_problems(self._current_problem_set, per_line=5)
            
            show_answers = input("\n是否显示答案？(y/n): ").strip().lower()
            if show_answers == 'y':
                print("\n--- 参考答案 ---")
                self._print_service.print_answers(self._current_problem_set, per_line=5)

    def _start_interactive_practice(self) -> None:
        """启动交互练习模式"""
        if self._current_problem_set is None:
            print("\n请先生成练习题！")
            return
        
        practice = InteractivePractice(self._current_problem_set)
        practice.start()

    def _exit_system(self) -> None:
        """退出系统"""
        print("\n" + "=" * 60)
        print("          谢 谢 使 用 口 算 练 习 系 统")
        print("=" * 60)
        print("                    再 见！")
        print("")


def main():
    """主程序入口"""
    menu = MenuSystem()
    menu.run()


if __name__ == "__main__":
    main()