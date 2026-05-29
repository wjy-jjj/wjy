"""
口算练习系统 - GUI单元测试
使用pytest和tkinter测试框架
"""

import pytest
import tkinter as tk
from tkinter import ttk

from gui import MathPracticeGUI
from src.core import ProblemSetFactory, ProblemSet


class TestMathPracticeGUI:
    """图形界面单元测试"""

    @pytest.fixture
    def app(self):
        """创建GUI应用实例"""
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        app = MathPracticeGUI(root)
        yield app
        root.destroy()

    def test_initialization(self, app):
        """测试初始化"""
        assert app.current_problem_set is None
        assert app.current_problem_index == 0
        assert app.correct_count == 0
        assert app.wrong_count == 0
        assert len(app.wrong_problems) == 0

    def test_generate_standard_problems(self, app):
        """测试生成标准练习题"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "10")
        app.problem_type.set("standard")
        
        app._generate_problems()
        
        assert app.current_problem_set is not None
        assert app.current_problem_set.count() == 10
        assert "已生成 10 道题" in app.status_label.cget("text")

    def test_generate_addition_problems(self, app):
        """测试生成加法练习题"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "10")
        app.problem_type.set("addition")
        
        app._generate_problems()
        
        assert app.current_problem_set is not None
        assert app.current_problem_set.count() == 10

    def test_generate_subtraction_problems(self, app):
        """测试生成减法练习题"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "10")
        app.problem_type.set("subtraction")
        
        app._generate_problems()
        
        assert app.current_problem_set is not None
        assert app.current_problem_set.count() == 10

    def test_generate_multiplication_problems(self, app):
        """测试生成乘法练习题"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "10")
        app.problem_type.set("multiplication")
        
        app._generate_problems()
        
        assert app.current_problem_set is not None
        assert app.current_problem_set.count() == 10

    def test_generate_mixed_problems(self, app):
        """测试生成混合练习题"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "10")
        app.problem_type.set("mixed")
        
        app._generate_problems()
        
        assert app.current_problem_set is not None
        assert app.current_problem_set.count() == 10

    def test_invalid_problem_count(self, app):
        """测试无效题目数量"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "0")
        
        app._generate_problems()
        
        assert app.current_problem_set is None

    def test_non_numeric_problem_count(self, app):
        """测试非数字题目数量"""
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "abc")
        
        app._generate_problems()
        
        assert app.current_problem_set is None

    def test_start_practice_without_problems(self, app):
        """测试没有题目时开始练习"""
        # 模拟开始练习
        result = app._start_practice()
        # 应该显示警告但不会崩溃
        assert result is None
        assert app.current_problem_index == 0

    def test_start_practice_with_problems(self, app):
        """测试有题目时开始练习"""
        # 先生成题目
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "5")
        app.problem_type.set("standard")
        app._generate_problems()
        
        # 开始练习
        app._start_practice()
        
        assert app.current_problem_index == 0
        assert app.correct_count == 0
        assert app.wrong_count == 0

    def test_submit_correct_answer(self, app):
        """测试提交正确答案"""
        # 生成题目并开始练习
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "1")
        app.problem_type.set("addition")
        app._generate_problems()
        app._start_practice()
        
        # 获取正确答案
        problem = app.current_problem_set[0]
        correct_answer = problem.answer
        
        # 提交答案
        app.answer_entry.delete(0, tk.END)
        app.answer_entry.insert(0, str(correct_answer))
        app._submit_answer()
        
        assert app.correct_count == 1
        assert app.wrong_count == 0

    def test_submit_wrong_answer(self, app):
        """测试提交错误答案"""
        # 生成题目并开始练习
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "1")
        app.problem_type.set("addition")
        app._generate_problems()
        app._start_practice()
        
        # 获取正确答案并提交错误答案
        problem = app.current_problem_set[0]
        wrong_answer = problem.answer + 1
        
        app.answer_entry.delete(0, tk.END)
        app.answer_entry.insert(0, str(wrong_answer))
        app._submit_answer()
        
        assert app.correct_count == 0
        assert app.wrong_count == 1
        assert len(app.wrong_problems) == 1

    def test_submit_invalid_answer(self, app):
        """测试提交无效答案"""
        # 生成题目并开始练习
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "1")
        app.problem_type.set("addition")
        app._generate_problems()
        app._start_practice()
        
        # 提交非数字答案
        app.answer_entry.delete(0, tk.END)
        app.answer_entry.insert(0, "abc")
        app._submit_answer()
        
        # 不应改变计数
        assert app.correct_count == 0
        assert app.wrong_count == 0

    def test_reset_practice(self, app):
        """测试重置练习"""
        # 生成题目并开始练习
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "5")
        app.problem_type.set("addition")
        app._generate_problems()
        app._start_practice()
        
        # 提交一个正确答案
        problem = app.current_problem_set[0]
        app.answer_entry.delete(0, tk.END)
        app.answer_entry.insert(0, str(problem.answer))
        app._submit_answer()
        
        assert app.correct_count == 1
        
        # 重置练习
        app._reset_practice()
        
        assert app.current_problem_index == 0
        assert app.correct_count == 0
        assert app.wrong_count == 0
        assert len(app.wrong_problems) == 0

    def test_update_progress(self, app):
        """测试更新进度"""
        # 生成题目
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "5")
        app.problem_type.set("addition")
        app._generate_problems()
        
        # 开始练习
        app._start_practice()
        
        assert app.progress_label.cget("text") == "0/5"
        
        # 提交一个答案
        problem = app.current_problem_set[0]
        app.answer_entry.delete(0, tk.END)
        app.answer_entry.insert(0, str(problem.answer))
        app._submit_answer()
        
        assert app.progress_label.cget("text") == "1/5"

    def test_refresh_view_empty(self, app):
        """测试刷新空视图"""
        app._refresh_view()
        
        text = app.problems_text.get(1.0, tk.END)
        assert "请先生成练习题" in text

    def test_refresh_view_with_problems(self, app):
        """测试刷新有题目时的视图"""
        # 生成题目
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "5")
        app.problem_type.set("addition")
        app._generate_problems()
        
        # 刷新视图
        app._refresh_view()
        
        text = app.problems_text.get(1.0, tk.END)
        assert "请先生成练习题" not in text
        assert "总题数: 5" in app.stats_label.cget("text")

    def test_update_result_display(self, app):
        """测试更新结果显示"""
        # 生成题目
        app.count_entry.delete(0, tk.END)
        app.count_entry.insert(0, "5")
        app.problem_type.set("addition")
        app._generate_problems()
        
        # 更新结果显示
        app._update_result_display()
        
        text = app.result_text.get(1.0, tk.END)
        assert text.strip() != ""


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])