"""
口算练习系统 - 图形界面版本
使用Tkinter创建友好的用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, List

from src.core import (
    ProblemSetFactory,
    ProblemSet,
    Problem,
    OperationType,
)


class MathPracticeGUI:
    """口算练习系统图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("口算练习系统")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.current_problem_set: Optional[ProblemSet] = None
        self.current_problem_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.wrong_problems: List[Problem] = []

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """设置界面样式"""
        self.style = ttk.Style()
        self.style.configure("Header.TLabel", font=("微软雅黑", 16, "bold"))
        self.style.configure("Title.TLabel", font=("微软雅黑", 12, "bold"))
        self.style.configure("Button.TButton", font=("微软雅黑", 10))
        self.style.configure("Status.TLabel", font=("微软雅黑", 9))

    def _create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部标题栏
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        self.header_label = ttk.Label(header_frame, text="口算练习系统", style="Header.TLabel")
        self.header_label.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header_frame, text="就绪", style="Status.TLabel", foreground="green")
        self.status_label.pack(side=tk.RIGHT)

        # 选项卡控制
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 生成题目选项卡
        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_tab, text="生成练习题")
        self._create_generate_tab()

        # 交互练习选项卡
        self.practice_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.practice_tab, text="交互练习")
        self._create_practice_tab()

        # 题目浏览选项卡
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="题目浏览")
        self._create_view_tab()

    def _create_generate_tab(self):
        """创建生成题目选项卡"""
        frame = ttk.LabelFrame(self.generate_tab, text="选择题目类型", padding="10")
        frame.pack(fill=tk.X, padx=10, pady=10)

        # 题目类型选择
        types = [
            ("标准练习（加减法混合）", "standard"),
            ("加法练习", "addition"),
            ("减法练习", "subtraction"),
            ("乘法练习", "multiplication"),
            ("混合练习（含乘法）", "mixed"),
        ]
        
        self.problem_type = tk.StringVar(value="standard")
        for text, value in types:
            ttk.Radiobutton(frame, text=text, variable=self.problem_type, value=value).pack(anchor=tk.W, pady=2)

        # 题目数量输入
        count_frame = ttk.Frame(self.generate_tab)
        count_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(count_frame, text="题目数量:").pack(side=tk.LEFT)
        self.count_entry = ttk.Entry(count_frame, width=10)
        self.count_entry.insert(0, "50")
        self.count_entry.pack(side=tk.LEFT, padx=5)
        
        self.generate_btn = ttk.Button(
            count_frame, text="生成题目", command=self._generate_problems, style="Button.TButton"
        )
        self.generate_btn.pack(side=tk.RIGHT)

        # 生成结果显示
        result_frame = ttk.LabelFrame(self.generate_tab, text="生成结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def _create_practice_tab(self):
        """创建交互练习选项卡"""
        # 练习区域
        practice_frame = ttk.LabelFrame(self.practice_tab, text="练习区", padding="20")
        practice_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 题目显示
        self.problem_display = ttk.Label(
            practice_frame, text="请先生成练习题", font=("微软雅黑", 24, "bold")
        )
        self.problem_display.pack(pady=20)

        # 答案输入
        answer_frame = ttk.Frame(practice_frame)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="答案:").pack(side=tk.LEFT, padx=5)
        self.answer_entry = ttk.Entry(answer_frame, width=15, font=("微软雅黑", 16))
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self._submit_answer)
        
        self.submit_btn = ttk.Button(
            answer_frame, text="提交", command=self._submit_answer, style="Button.TButton"
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        # 反馈标签
        self.feedback_label = ttk.Label(practice_frame, text="", font=("微软雅黑", 12))
        self.feedback_label.pack(pady=10)

        # 进度显示
        progress_frame = ttk.Frame(practice_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(progress_frame, text="进度:").pack(side=tk.LEFT)
        self.progress_label = ttk.Label(progress_frame, text="0/0")
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(progress_frame, text="|").pack(side=tk.LEFT, padx=5)
        ttk.Label(progress_frame, text="正确:").pack(side=tk.LEFT)
        self.correct_label = ttk.Label(progress_frame, text="0", foreground="green")
        self.correct_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(progress_frame, text="|").pack(side=tk.LEFT, padx=5)
        ttk.Label(progress_frame, text="错误:").pack(side=tk.LEFT)
        self.wrong_label = ttk.Label(progress_frame, text="0", foreground="red")
        self.wrong_label.pack(side=tk.LEFT, padx=5)

        # 开始/重置按钮
        action_frame = ttk.Frame(self.practice_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = ttk.Button(
            action_frame, text="开始练习", command=self._start_practice, style="Button.TButton"
        )
        self.start_btn.pack(side=tk.LEFT)
        
        self.reset_btn = ttk.Button(
            action_frame, text="重置练习", command=self._reset_practice, style="Button.TButton"
        )
        self.reset_btn.pack(side=tk.RIGHT)

        # 练习结果区域
        result_frame = ttk.LabelFrame(self.practice_tab, text="练习结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.practice_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.practice_result.pack(fill=tk.BOTH, expand=True)

    def _create_view_tab(self):
        """创建题目浏览选项卡"""
        # 题目列表
        view_frame = ttk.LabelFrame(self.view_tab, text="题目列表", padding="10")
        view_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.problems_text = scrolledtext.ScrolledText(view_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.problems_text.pack(fill=tk.BOTH, expand=True)

        # 答案显示
        answer_frame = ttk.LabelFrame(self.view_tab, text="参考答案", padding="10")
        answer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.answers_text = scrolledtext.ScrolledText(answer_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.answers_text.pack(fill=tk.BOTH, expand=True)

        # 统计信息
        stats_frame = ttk.LabelFrame(self.view_tab, text="统计信息", padding="10")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="请先生成练习题")
        self.stats_label.pack()

        # 按钮
        btn_frame = ttk.Frame(self.view_tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="刷新显示", command=self._refresh_view, style="Button.TButton").pack(side=tk.LEFT)

    def _generate_problems(self):
        """生成练习题"""
        try:
            count = int(self.count_entry.get())
            if count <= 0 or count > 200:
                messagebox.showerror("错误", "题目数量应在1-200之间")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return

        problem_type = self.problem_type.get()
        
        try:
            if problem_type == "standard":
                self.current_problem_set = ProblemSetFactory.create_standard_set(count)
            elif problem_type == "addition":
                self.current_problem_set = ProblemSetFactory.create_addition_only(count)
            elif problem_type == "subtraction":
                self.current_problem_set = ProblemSetFactory.create_subtraction_only(count)
            elif problem_type == "multiplication":
                self.current_problem_set = ProblemSetFactory.create_multiplication_set(count)
            elif problem_type == "mixed":
                self.current_problem_set = ProblemSetFactory.create_mixed_set(count, include_multiplication=True)

            self.status_label.config(text=f"已生成 {count} 道题", foreground="green")
            self._update_result_display()
            self._refresh_view()
            messagebox.showinfo("成功", f"已成功生成 {count} 道练习题！")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成题目失败: {str(e)}")

    def _update_result_display(self):
        """更新生成结果显示"""
        if self.current_problem_set is None:
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        problems = self.current_problem_set.get_problems()
        lines = []
        for i, problem in enumerate(problems, 1):
            lines.append(f"{i}. {problem}")
        
        self.result_text.insert(tk.END, "\n".join(lines))
        self.result_text.config(state=tk.DISABLED)

    def _refresh_view(self):
        """刷新题目浏览视图"""
        if self.current_problem_set is None:
            self.problems_text.config(state=tk.NORMAL)
            self.problems_text.delete(1.0, tk.END)
            self.problems_text.insert(tk.END, "请先生成练习题")
            self.problems_text.config(state=tk.DISABLED)
            
            self.answers_text.config(state=tk.NORMAL)
            self.answers_text.delete(1.0, tk.END)
            self.answers_text.insert(tk.END, "请先生成练习题")
            self.answers_text.config(state=tk.DISABLED)
            
            self.stats_label.config(text="请先生成练习题")
            return

        problems = self.current_problem_set.get_problems()
        
        # 更新题目列表
        self.problems_text.config(state=tk.NORMAL)
        self.problems_text.delete(1.0, tk.END)
        for i, problem in enumerate(problems, 1):
            self.problems_text.insert(tk.END, f"{i}. {problem}\n")
        self.problems_text.config(state=tk.DISABLED)

        # 更新答案列表
        self.answers_text.config(state=tk.NORMAL)
        self.answers_text.delete(1.0, tk.END)
        for i, problem in enumerate(problems, 1):
            self.answers_text.insert(tk.END, f"{i}. {problem.with_answer()}\n")
        self.answers_text.config(state=tk.DISABLED)

        # 更新统计信息
        addition_count = self.current_problem_set.count_by_operation(OperationType.ADDITION)
        subtraction_count = self.current_problem_set.count_by_operation(OperationType.SUBTRACTION)
        multiplication_count = self.current_problem_set.count_by_operation(OperationType.MULTIPLICATION)
        
        stats = f"总题数: {self.current_problem_set.count()} | "
        stats += f"加法: {addition_count} | "
        stats += f"减法: {subtraction_count} | "
        stats += f"乘法: {multiplication_count}"
        self.stats_label.config(text=stats)

    def _start_practice(self):
        """开始练习"""
        if self.current_problem_set is None:
            messagebox.showwarning("警告", "请先生成练习题！")
            return

        self.current_problem_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.wrong_problems = []
        
        self._update_progress()
        self._display_current_problem()
        
        self.answer_entry.focus_set()
        
        self.practice_result.config(state=tk.NORMAL)
        self.practice_result.delete(1.0, tk.END)
        self.practice_result.config(state=tk.DISABLED)

    def _reset_practice(self):
        """重置练习"""
        self.current_problem_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.wrong_problems = []
        
        self.problem_display.config(text="请先生成练习题")
        self.feedback_label.config(text="")
        self._update_progress()
        
        self.practice_result.config(state=tk.NORMAL)
        self.practice_result.delete(1.0, tk.END)
        self.practice_result.config(state=tk.DISABLED)

    def _display_current_problem(self):
        """显示当前题目"""
        if self.current_problem_set is None:
            return

        if self.current_problem_index >= self.current_problem_set.count():
            self._show_practice_summary()
            return

        problem = self.current_problem_set[self.current_problem_index]
        self.problem_display.config(text=f"{self.current_problem_index + 1}. {problem}")
        self.answer_entry.delete(0, tk.END)

    def _submit_answer(self, event=None):
        """提交答案"""
        if self.current_problem_set is None:
            return

        if self.current_problem_index >= self.current_problem_set.count():
            return

        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字")
            return

        problem = self.current_problem_set[self.current_problem_index]
        
        if user_answer == problem.answer:
            self.correct_count += 1
            self.feedback_label.config(text="✓ 正确！", foreground="green")
        else:
            self.wrong_count += 1
            self.wrong_problems.append(problem)
            self.feedback_label.config(text=f"✗ 错误！正确答案是 {problem.answer}", foreground="red")

        self.current_problem_index += 1
        self._update_progress()
        self._display_current_problem()

    def _update_progress(self):
        """更新进度显示"""
        if self.current_problem_set is None:
            self.progress_label.config(text="0/0")
            self.correct_label.config(text="0")
            self.wrong_label.config(text="0")
            return

        total = self.current_problem_set.count()
        self.progress_label.config(text=f"{self.current_problem_index}/{total}")
        self.correct_label.config(text=str(self.correct_count))
        self.wrong_label.config(text=str(self.wrong_count))

    def _show_practice_summary(self):
        """显示练习总结"""
        total = self.correct_count + self.wrong_count
        accuracy = (self.correct_count / total) * 100 if total > 0 else 0
        
        summary = f"练习完成！\n\n"
        summary += f"总题数: {total} 道\n"
        summary += f"正确: {self.correct_count} 道\n"
        summary += f"错误: {self.wrong_count} 道\n"
        summary += f"正确率: {accuracy:.1f}%\n\n"
        
        if accuracy >= 90:
            summary += "🎉 太棒了！继续保持！"
        elif accuracy >= 70:
            summary += "👍 不错！继续努力！"
        elif accuracy >= 60:
            summary += "💪 需要多加练习！"
        else:
            summary += "📚 加油！多做练习会更好！"

        self.problem_display.config(text="练习完成！")
        
        self.practice_result.config(state=tk.NORMAL)
        self.practice_result.delete(1.0, tk.END)
        self.practice_result.insert(tk.END, summary)
        
        if self.wrong_problems:
            self.practice_result.insert(tk.END, "\n\n--- 错题回顾 ---\n")
            for i, problem in enumerate(self.wrong_problems, 1):
                self.practice_result.insert(tk.END, f"{i}. {problem.with_answer()}\n")
        
        self.practice_result.config(state=tk.DISABLED)
        
        messagebox.showinfo("练习完成", summary)


def main():
    """主程序入口"""
    root = tk.Tk()
    app = MathPracticeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()