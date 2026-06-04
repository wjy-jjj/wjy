"""
数据库单元测试
测试数据库操作的各个DAO类
"""

import unittest
import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import (
    DatabaseManager,
    UserDAO,
    ClassDAO,
    ProblemSetDAO,
    ProblemDAO,
    PracticeRecordDAO,
    AnswerRecordDAO
)

class TestDatabaseManager(unittest.TestCase):
    """测试数据库连接管理器"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
    
    def test_singleton(self):
        """测试单例模式"""
        another_manager = DatabaseManager()
        self.assertIs(self.db_manager, another_manager)
    
    def test_connection(self):
        """测试数据库连接"""
        with self.db_manager.get_connection() as conn:
            self.assertIsNotNone(conn)
            self.assertIsInstance(conn, sqlite3.Connection)

class TestUserDAO(unittest.TestCase):
    """测试用户数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.user_dao = UserDAO(self.db_manager)
    
    def test_create_user(self):
        """测试创建用户"""
        user_id = self.user_dao.create_user(
            'test_user', 'test_pass', 'student', '测试用户'
        )
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
    
    def test_get_user_by_username(self):
        """测试根据用户名获取用户"""
        self.user_dao.create_user('get_user_test', 'pass', 'student', '获取测试')
        user = self.user_dao.get_user_by_username('get_user_test')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'get_user_test')
        self.assertEqual(user['real_name'], '获取测试')
    
    def test_get_user_by_id(self):
        """测试根据ID获取用户"""
        user_id = self.user_dao.create_user('get_id_test', 'pass', 'student', 'ID测试')
        user = self.user_dao.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['user_id'], user_id)
    
    def test_update_user(self):
        """测试更新用户"""
        user_id = self.user_dao.create_user('update_test', 'pass', 'student', '更新前')
        rows_updated = self.user_dao.update_user(user_id, real_name='更新后')
        self.assertEqual(rows_updated, 1)
        
        user = self.user_dao.get_user_by_id(user_id)
        self.assertEqual(user['real_name'], '更新后')
    
    def test_delete_user(self):
        """测试删除用户"""
        user_id = self.user_dao.create_user('delete_test', 'pass', 'student', '删除测试')
        rows_deleted = self.user_dao.delete_user(user_id)
        self.assertEqual(rows_deleted, 1)
        
        user = self.user_dao.get_user_by_id(user_id)
        self.assertIsNone(user)
    
    def test_get_all_users(self):
        """测试获取所有用户"""
        self.user_dao.create_user('all_user_1', 'pass', 'student', '用户1')
        self.user_dao.create_user('all_user_2', 'pass', 'teacher', '用户2')
        
        users = self.user_dao.get_all_users()
        self.assertGreaterEqual(len(users), 2)
    
    def test_get_users_by_role(self):
        """测试按角色获取用户"""
        self.user_dao.create_user('role_student', 'pass', 'student', '学生')
        self.user_dao.create_user('role_teacher', 'pass', 'teacher', '老师')
        
        students = self.user_dao.get_all_users('student')
        teachers = self.user_dao.get_all_users('teacher')
        
        self.assertGreaterEqual(len(students), 1)
        self.assertGreaterEqual(len(teachers), 1)

class TestClassDAO(unittest.TestCase):
    """测试班级数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.class_dao = ClassDAO(self.db_manager)
        self.user_dao = UserDAO(self.db_manager)
    
    def test_create_class(self):
        """测试创建班级"""
        class_id = self.class_dao.create_class('测试班级', None, '三年级')
        self.assertIsInstance(class_id, int)
        self.assertGreater(class_id, 0)
    
    def test_get_class_by_name(self):
        """测试根据名称获取班级"""
        self.class_dao.create_class('名称测试班', None, '四年级')
        cls = self.class_dao.get_class_by_name('名称测试班')
        self.assertIsNotNone(cls)
        self.assertEqual(cls['class_name'], '名称测试班')
    
    def test_update_class(self):
        """测试更新班级"""
        class_id = self.class_dao.create_class('更新测试班', None, '五年级')
        teacher_id = self.user_dao.create_user('teacher_update', 'pass', 'teacher', '李老师')
        
        rows_updated = self.class_dao.update_class(class_id, teacher_id=teacher_id, grade='六年级')
        self.assertEqual(rows_updated, 1)
        
        cls = self.class_dao.get_class_by_id(class_id)
        self.assertEqual(cls['teacher_id'], teacher_id)
        self.assertEqual(cls['grade'], '六年级')

class TestProblemSetDAO(unittest.TestCase):
    """测试题目集数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.problem_set_dao = ProblemSetDAO(self.db_manager)
    
    def test_create_set(self):
        """测试创建题目集"""
        set_id = self.problem_set_dao.create_set(
            '测试题目集', 'addition', 10, 1, 10, '测试描述'
        )
        self.assertIsInstance(set_id, int)
        self.assertGreater(set_id, 0)
    
    def test_get_set_by_id(self):
        """测试根据ID获取题目集"""
        set_id = self.problem_set_dao.create_set('获取测试集', 'subtraction', 20, 1, 50)
        problem_set = self.problem_set_dao.get_set_by_id(set_id)
        
        self.assertIsNotNone(problem_set)
        self.assertEqual(problem_set['name'], '获取测试集')
        self.assertEqual(problem_set['operation_type'], 'subtraction')
    
    def test_get_all_sets(self):
        """测试获取所有题目集"""
        self.problem_set_dao.create_set('集1', 'addition', 10)
        self.problem_set_dao.create_set('集2', 'multiplication', 15)
        
        sets = self.problem_set_dao.get_all_sets()
        self.assertGreaterEqual(len(sets), 2)
    
    def test_delete_set(self):
        """测试删除题目集"""
        set_id = self.problem_set_dao.create_set('删除测试集', 'addition', 10)
        rows_deleted = self.problem_set_dao.delete_set(set_id)
        
        self.assertGreaterEqual(rows_deleted, 0)
        
        problem_set = self.problem_set_dao.get_set_by_id(set_id)
        self.assertIsNone(problem_set)

class TestProblemDAO(unittest.TestCase):
    """测试题目数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.problem_set_dao = ProblemSetDAO(self.db_manager)
        self.problem_dao = ProblemDAO(self.db_manager)
    
    def test_create_problem(self):
        """测试创建题目"""
        set_id = self.problem_set_dao.create_set('题目测试集', 'addition', 10)
        problem_id = self.problem_dao.create_problem(
            set_id, 3, 5, '+', 8, 1, 1
        )
        
        self.assertIsInstance(problem_id, int)
        self.assertGreater(problem_id, 0)
    
    def test_create_problems_batch(self):
        """测试批量创建题目"""
        set_id = self.problem_set_dao.create_set('批量测试集', 'addition', 5)
        problems = [
            {'operand1': 1, 'operand2': 2, 'operation': '+', 'answer': 3},
            {'operand1': 4, 'operand2': 5, 'operation': '+', 'answer': 9},
            {'operand1': 7, 'operand2': 8, 'operation': '+', 'answer': 15},
        ]
        
        self.problem_dao.create_problems_batch(set_id, problems)
        all_problems = self.problem_dao.get_problems_by_set(set_id)
        
        self.assertEqual(len(all_problems), 3)
        self.assertEqual(all_problems[0]['operand1'], 1)
        self.assertEqual(all_problems[1]['answer'], 9)
    
    def test_get_problems_by_set(self):
        """测试获取题目集的所有题目"""
        set_id = self.problem_set_dao.create_set('获取题目集', 'subtraction', 3)
        self.problem_dao.create_problem(set_id, 10, 3, '-', 7, 1, 1)
        self.problem_dao.create_problem(set_id, 15, 5, '-', 10, 1, 2)
        
        problems = self.problem_dao.get_problems_by_set(set_id)
        self.assertEqual(len(problems), 2)

class TestPracticeRecordDAO(unittest.TestCase):
    """测试练习记录数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.user_dao = UserDAO(self.db_manager)
        self.practice_record_dao = PracticeRecordDAO(self.db_manager)
    
    def test_create_record(self):
        """测试创建练习记录"""
        user_id = self.user_dao.create_user('practice_user', 'pass', 'student', '练习用户')
        record_id = self.practice_record_dao.create_record(user_id, 10)
        
        self.assertIsInstance(record_id, int)
        self.assertGreater(record_id, 0)
    
    def test_update_record(self):
        """测试更新练习记录"""
        user_id = self.user_dao.create_user('update_record_user', 'pass', 'student', '更新记录用户')
        record_id = self.practice_record_dao.create_record(user_id, 10)
        
        rows_updated = self.practice_record_dao.update_record(
            record_id, correct_count=8, wrong_count=2, score=80, duration=300
        )
        
        self.assertEqual(rows_updated, 1)
        
        record = self.practice_record_dao.get_record_by_id(record_id)
        self.assertEqual(record['correct_count'], 8)
        self.assertEqual(record['score'], 80)
    
    def test_get_records_by_user(self):
        """测试获取用户的练习记录"""
        user_id = self.user_dao.create_user('records_user', 'pass', 'student', '记录用户')
        self.practice_record_dao.create_record(user_id, 10)
        self.practice_record_dao.create_record(user_id, 20)
        
        records = self.practice_record_dao.get_records_by_user(user_id)
        self.assertEqual(len(records), 2)
    
    def test_get_student_statistics(self):
        """测试获取学生统计"""
        user_id = self.user_dao.create_user('stats_user', 'pass', 'student', '统计用户')
        self.practice_record_dao.create_record(user_id, 10)
        self.practice_record_dao.update_record(1, correct_count=8, wrong_count=2, score=80)
        
        stats = self.practice_record_dao.get_student_statistics(user_id)
        self.assertIsNotNone(stats)
        self.assertEqual(stats['practice_count'], 1)
        self.assertEqual(stats['avg_score'], 80.0)

class TestAnswerRecordDAO(unittest.TestCase):
    """测试答题记录数据访问对象"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        self.user_dao = UserDAO(self.db_manager)
        self.problem_set_dao = ProblemSetDAO(self.db_manager)
        self.problem_dao = ProblemDAO(self.db_manager)
        self.practice_record_dao = PracticeRecordDAO(self.db_manager)
        self.answer_record_dao = AnswerRecordDAO(self.db_manager)
    
    def test_create_answer(self):
        """测试创建答题记录"""
        user_id = self.user_dao.create_user('answer_user', 'pass', 'student', '答题用户')
        set_id = self.problem_set_dao.create_set('答题测试集', 'addition', 1)
        problem_id = self.problem_dao.create_problem(set_id, 2, 3, '+', 5, 1, 1)
        record_id = self.practice_record_dao.create_record(user_id, 1)
        
        answer_id = self.answer_record_dao.create_answer(record_id, problem_id, 5, True, 5)
        
        self.assertIsInstance(answer_id, int)
        self.assertGreater(answer_id, 0)
    
    def test_create_answers_batch(self):
        """测试批量创建答题记录"""
        user_id = self.user_dao.create_user('batch_answer_user', 'pass', 'student', '批量答题用户')
        set_id = self.problem_set_dao.create_set('批量答题集', 'addition', 3)
        self.problem_dao.create_problem(set_id, 1, 1, '+', 2, 1, 1)
        self.problem_dao.create_problem(set_id, 2, 2, '+', 4, 1, 2)
        record_id = self.practice_record_dao.create_record(user_id, 2)
        
        answers = [
            {'problem_id': 1, 'user_answer': 2, 'is_correct': True, 'time_spent': 3},
            {'problem_id': 2, 'user_answer': 5, 'is_correct': False, 'time_spent': 4},
        ]
        
        self.answer_record_dao.create_answers_batch(record_id, answers)
        all_answers = self.answer_record_dao.get_answers_by_record(record_id)
        
        self.assertEqual(len(all_answers), 2)
    
    def test_get_wrong_problems_statistics(self):
        """测试获取错题统计"""
        # 创建测试数据
        user_id = self.user_dao.create_user('wrong_stats_user', 'pass', 'student', '错题统计用户')
        set_id = self.problem_set_dao.create_set('错题统计集', 'addition', 2)
        problem1_id = self.problem_dao.create_problem(set_id, 10, 5, '+', 15, 1, 1)
        problem2_id = self.problem_dao.create_problem(set_id, 20, 8, '+', 28, 1, 2)
        
        # 创建多次练习记录
        for i in range(5):
            record_id = self.practice_record_dao.create_record(user_id, 2)
            # 第一题：3次正确，2次错误
            self.answer_record_dao.create_answer(record_id, problem1_id, 15 if i < 3 else 14, i < 3, 5)
            # 第二题：1次正确，4次错误
            self.answer_record_dao.create_answer(record_id, problem2_id, 28 if i == 0 else 27, i == 0, 5)
        
        stats = self.answer_record_dao.get_wrong_problems_statistics()
        self.assertGreaterEqual(len(stats), 2)
        
        # 验证第二题错误率更高
        if len(stats) >= 2:
            self.assertGreater(stats[0]['wrong_rate'], stats[1]['wrong_rate'])

class TestDatabaseIntegration(unittest.TestCase):
    """测试数据库集成"""
    
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        
        self.user_dao = UserDAO(self.db_manager)
        self.class_dao = ClassDAO(self.db_manager)
        self.problem_set_dao = ProblemSetDAO(self.db_manager)
        self.problem_dao = ProblemDAO(self.db_manager)
        self.practice_record_dao = PracticeRecordDAO(self.db_manager)
        self.answer_record_dao = AnswerRecordDAO(self.db_manager)
    
    def test_full_workflow(self):
        """测试完整的练习流程"""
        # 1. 创建老师和班级
        teacher_id = self.user_dao.create_user('teacher_wf', 'pass', 'teacher', '王老师')
        class_id = self.class_dao.create_class('三年级二班', teacher_id, '三年级')
        
        # 2. 创建学生
        student_id = self.user_dao.create_user('student_wf', 'pass', 'student', '小华', class_id)
        
        # 3. 创建题目集和题目
        set_id = self.problem_set_dao.create_set('加法练习', 'addition', 3, 1, 20)
        problems = [
            {'operand1': 5, 'operand2': 7, 'operation': '+', 'answer': 12},
            {'operand1': 8, 'operand2': 9, 'operation': '+', 'answer': 17},
            {'operand1': 12, 'operand2': 6, 'operation': '+', 'answer': 18},
        ]
        self.problem_dao.create_problems_batch(set_id, problems)
        
        # 4. 创建练习记录
        record_id = self.practice_record_dao.create_record(student_id, 3, set_id)
        
        # 5. 创建答题记录
        answer_records = [
            {'problem_id': 1, 'user_answer': 12, 'is_correct': True, 'time_spent': 4},
            {'problem_id': 2, 'user_answer': 16, 'is_correct': False, 'time_spent': 5},
            {'problem_id': 3, 'user_answer': 18, 'is_correct': True, 'time_spent': 3},
        ]
        self.answer_record_dao.create_answers_batch(record_id, answer_records)
        
        # 6. 更新练习记录统计
        self.practice_record_dao.update_record(
            record_id,
            correct_count=2,
            wrong_count=1,
            score=67,
            duration=12,
            end_time='2024-01-15 10:30:00'
        )
        
        # 7. 验证数据完整性
        student = self.user_dao.get_user_by_id(student_id)
        self.assertEqual(student['class_id'], class_id)
        
        record = self.practice_record_dao.get_record_by_id(record_id)
        self.assertEqual(record['correct_count'], 2)
        self.assertEqual(record['score'], 67)
        
        answers = self.answer_record_dao.get_answers_by_record(record_id)
        self.assertEqual(len(answers), 3)
        
        # 8. 获取班级统计
        class_stats = self.practice_record_dao.get_class_statistics(class_id)
        self.assertIsNotNone(class_stats)
        
        print("完整流程测试通过！")

if __name__ == '__main__':
    # 创建测试数据库目录
    os.makedirs('data', exist_ok=True)
    
    # 运行所有测试
    unittest.main(verbosity=2)