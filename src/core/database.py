"""
数据库操作模块
提供SQLite数据库的连接管理和数据访问功能
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, Dict, List, Any
from datetime import datetime

class DatabaseManager:
    """数据库连接管理器"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接（使用上下文管理器）"""
        if self._connection is None:
            # 确保数据目录存在
            os.makedirs('data', exist_ok=True)
            self._connection = sqlite3.connect('data/practice.db')
            self._connection.row_factory = sqlite3.Row
            # 设置WAL模式提高并发性能
            self._connection.execute('PRAGMA journal_mode=WAL;')
            self._connection.execute('PRAGMA synchronous=NORMAL;')
        try:
            yield self._connection
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            raise
    
    def close_connection(self):
        """关闭数据库连接"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def init_database(self):
        """初始化数据库表结构"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'student',
                    real_name VARCHAR(50),
                    class_id INTEGER,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (class_id) REFERENCES classes(class_id)
                )
            ''')
            
            # 班级表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classes (
                    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_name VARCHAR(50) NOT NULL UNIQUE,
                    teacher_id INTEGER,
                    grade VARCHAR(20),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES users(user_id)
                )
            ''')
            
            # 题目集表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problem_sets (
                    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    operation_type VARCHAR(20) NOT NULL,
                    problem_count INTEGER NOT NULL DEFAULT 50,
                    min_value INTEGER NOT NULL DEFAULT 1,
                    max_value INTEGER NOT NULL DEFAULT 100,
                    created_by INTEGER,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(user_id)
                )
            ''')
            
            # 题目表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problems (
                    problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    set_id INTEGER NOT NULL,
                    operand1 INTEGER NOT NULL,
                    operand2 INTEGER NOT NULL,
                    operation VARCHAR(10) NOT NULL,
                    answer INTEGER NOT NULL,
                    difficulty INTEGER DEFAULT 1,
                    order_num INTEGER NOT NULL,
                    FOREIGN KEY (set_id) REFERENCES problem_sets(set_id)
                )
            ''')
            
            # 练习记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS practice_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    set_id INTEGER,
                    total_count INTEGER NOT NULL,
                    correct_count INTEGER NOT NULL DEFAULT 0,
                    wrong_count INTEGER NOT NULL DEFAULT 0,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    duration INTEGER,
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (set_id) REFERENCES problem_sets(set_id)
                )
            ''')
            
            # 答题记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answer_records (
                    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER NOT NULL,
                    problem_id INTEGER NOT NULL,
                    user_answer INTEGER,
                    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
                    time_spent INTEGER,
                    FOREIGN KEY (record_id) REFERENCES practice_records(record_id),
                    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_class_id ON users(class_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_classes_class_name ON classes(class_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_problem_sets_created_by ON problem_sets(created_by)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_problem_sets_operation_type ON problem_sets(operation_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_problems_set_id ON problems(set_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_practice_records_user_id ON practice_records(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_practice_records_start_time ON practice_records(start_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_answer_records_record_id ON answer_records(record_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_answer_records_problem_id ON answer_records(problem_id)')
            
            conn.commit()
            print("数据库初始化完成")

class UserDAO:
    """用户数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_user_by_id(self, user_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取用户"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
    
    def get_user_by_username(self, username: str) -> Optional[sqlite3.Row]:
        """根据用户名获取用户"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
    
    def create_user(self, username: str, password: str, role: str = 'student', 
                    real_name: Optional[str] = None, class_id: Optional[int] = None) -> int:
        """创建用户"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, role, real_name, class_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password, role, real_name, class_id))
            conn.commit()
            return cursor.lastrowid
    
    def update_user(self, user_id: int, **kwargs) -> int:
        """更新用户信息"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            kwargs['updated_at'] = datetime.now().isoformat()
            fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values()) + [user_id]
            cursor.execute(f"UPDATE users SET {fields} WHERE user_id = ?", values)
            conn.commit()
            return cursor.rowcount
    
    def delete_user(self, user_id: int) -> int:
        """删除用户"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount
    
    def get_students_by_class(self, class_id: int) -> List[sqlite3.Row]:
        """获取班级所有学生"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE class_id = ? AND role = 'student'", (class_id,))
            return cursor.fetchall()
    
    def get_all_users(self, role: Optional[str] = None) -> List[sqlite3.Row]:
        """获取所有用户"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            if role:
                cursor.execute("SELECT * FROM users WHERE role = ?", (role,))
            else:
                cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

class ClassDAO:
    """班级数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_class_by_id(self, class_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取班级"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classes WHERE class_id = ?", (class_id,))
            return cursor.fetchone()
    
    def get_class_by_name(self, class_name: str) -> Optional[sqlite3.Row]:
        """根据名称获取班级"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classes WHERE class_name = ?", (class_name,))
            return cursor.fetchone()
    
    def create_class(self, class_name: str, teacher_id: Optional[int] = None, 
                     grade: Optional[str] = None) -> int:
        """创建班级"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO classes (class_name, teacher_id, grade)
                VALUES (?, ?, ?)
            ''', (class_name, teacher_id, grade))
            conn.commit()
            return cursor.lastrowid
    
    def update_class(self, class_id: int, **kwargs) -> int:
        """更新班级信息"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values()) + [class_id]
            cursor.execute(f"UPDATE classes SET {fields} WHERE class_id = ?", values)
            conn.commit()
            return cursor.rowcount
    
    def delete_class(self, class_id: int) -> int:
        """删除班级"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM classes WHERE class_id = ?", (class_id,))
            conn.commit()
            return cursor.rowcount
    
    def get_all_classes(self) -> List[sqlite3.Row]:
        """获取所有班级"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classes")
            return cursor.fetchall()

class ProblemSetDAO:
    """题目集数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_set_by_id(self, set_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取题目集"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM problem_sets WHERE set_id = ?", (set_id,))
            return cursor.fetchone()
    
    def get_sets_by_user(self, user_id: int) -> List[sqlite3.Row]:
        """获取用户创建的题目集"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM problem_sets WHERE created_by = ?", (user_id,))
            return cursor.fetchall()
    
    def get_all_sets(self) -> List[sqlite3.Row]:
        """获取所有题目集"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM problem_sets ORDER BY created_at DESC")
            return cursor.fetchall()
    
    def create_set(self, name: str, operation_type: str, problem_count: int = 50,
                   min_value: int = 1, max_value: int = 100, description: Optional[str] = None,
                   created_by: Optional[int] = None) -> int:
        """创建题目集"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO problem_sets (name, description, operation_type, 
                                        problem_count, min_value, max_value, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, operation_type, problem_count, min_value, max_value, created_by))
            conn.commit()
            return cursor.lastrowid
    
    def update_set(self, set_id: int, **kwargs) -> int:
        """更新题目集"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values()) + [set_id]
            cursor.execute(f"UPDATE problem_sets SET {fields} WHERE set_id = ?", values)
            conn.commit()
            return cursor.rowcount
    
    def delete_set(self, set_id: int) -> int:
        """删除题目集（级联删除相关题目）"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM problems WHERE set_id = ?", (set_id,))
            cursor.execute("DELETE FROM problem_sets WHERE set_id = ?", (set_id,))
            conn.commit()
            return cursor.rowcount

class ProblemDAO:
    """题目数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_problem_by_id(self, problem_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM problems WHERE problem_id = ?", (problem_id,))
            return cursor.fetchone()
    
    def get_problems_by_set(self, set_id: int) -> List[sqlite3.Row]:
        """获取题目集的所有题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM problems WHERE set_id = ? ORDER BY order_num", (set_id,))
            return cursor.fetchall()
    
    def create_problem(self, set_id: int, operand1: int, operand2: int, operation: str,
                       answer: int, difficulty: int = 1, order_num: int = 1) -> int:
        """创建题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO problems (set_id, operand1, operand2, operation, 
                                     answer, difficulty, order_num)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (set_id, operand1, operand2, operation, answer, difficulty, order_num))
            conn.commit()
            return cursor.lastrowid
    
    def create_problems_batch(self, set_id: int, problems: List[Dict[str, Any]]) -> None:
        """批量创建题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            for idx, problem in enumerate(problems, 1):
                cursor.execute('''
                    INSERT INTO problems (set_id, operand1, operand2, operation, 
                                         answer, difficulty, order_num)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (set_id, problem['operand1'], problem['operand2'], problem['operation'],
                      problem['answer'], problem.get('difficulty', 1), idx))
            conn.commit()
    
    def delete_problems_by_set(self, set_id: int) -> int:
        """删除题目集的所有题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM problems WHERE set_id = ?", (set_id,))
            conn.commit()
            return cursor.rowcount

class PracticeRecordDAO:
    """练习记录数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_record_by_id(self, record_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取练习记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM practice_records WHERE record_id = ?", (record_id,))
            return cursor.fetchone()
    
    def get_records_by_user(self, user_id: int) -> List[sqlite3.Row]:
        """获取用户的练习记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM practice_records WHERE user_id = ? ORDER BY start_time DESC", (user_id,))
            return cursor.fetchall()
    
    def create_record(self, user_id: int, total_count: int, set_id: Optional[int] = None,
                      start_time: Optional[str] = None) -> int:
        """创建练习记录"""
        if start_time is None:
            start_time = datetime.now().isoformat()
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO practice_records (user_id, set_id, total_count, start_time)
                VALUES (?, ?, ?, ?)
            ''', (user_id, set_id, total_count, start_time))
            conn.commit()
            return cursor.lastrowid
    
    def update_record(self, record_id: int, **kwargs) -> int:
        """更新练习记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values()) + [record_id]
            cursor.execute(f"UPDATE practice_records SET {fields} WHERE record_id = ?", values)
            conn.commit()
            return cursor.rowcount
    
    def get_student_statistics(self, user_id: int) -> Optional[sqlite3.Row]:
        """获取学生练习统计"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(record_id) as practice_count,
                    AVG(score) as avg_score,
                    SUM(total_count) as total_problems,
                    SUM(correct_count) as correct_problems
                FROM practice_records
                WHERE user_id = ?
            ''', (user_id,))
            return cursor.fetchone()
    
    def get_class_statistics(self, class_id: int) -> Optional[sqlite3.Row]:
        """获取班级练习统计"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT pr.user_id) as student_count,
                    COUNT(pr.record_id) as total_practices,
                    AVG(pr.score) as avg_score
                FROM practice_records pr
                JOIN users u ON pr.user_id = u.user_id
                WHERE u.class_id = ?
            ''', (class_id,))
            return cursor.fetchone()

class AnswerRecordDAO:
    """答题记录数据访问对象"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_answer_by_id(self, answer_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取答题记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM answer_records WHERE answer_id = ?", (answer_id,))
            return cursor.fetchone()
    
    def get_answers_by_record(self, record_id: int) -> List[sqlite3.Row]:
        """获取练习记录的所有答题记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM answer_records WHERE record_id = ?", (record_id,))
            return cursor.fetchall()
    
    def create_answer(self, record_id: int, problem_id: int, user_answer: Optional[int] = None,
                      is_correct: bool = False, time_spent: Optional[int] = None) -> int:
        """创建答题记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO answer_records (record_id, problem_id, user_answer, is_correct, time_spent)
                VALUES (?, ?, ?, ?, ?)
            ''', (record_id, problem_id, user_answer, is_correct, time_spent))
            conn.commit()
            return cursor.lastrowid
    
    def create_answers_batch(self, record_id: int, answers: List[Dict[str, Any]]) -> None:
        """批量创建答题记录"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            for answer in answers:
                cursor.execute('''
                    INSERT INTO answer_records (record_id, problem_id, user_answer, is_correct, time_spent)
                    VALUES (?, ?, ?, ?, ?)
                ''', (record_id, answer['problem_id'], answer.get('user_answer'),
                      answer.get('is_correct', False), answer.get('time_spent')))
            conn.commit()
    
    def get_wrong_problems_statistics(self, limit: int = 10) -> List[sqlite3.Row]:
        """获取错误率最高的题目"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.problem_id,
                    p.operand1,
                    p.operation,
                    p.operand2,
                    p.answer,
                    COUNT(*) as total_attempts,
                    SUM(CASE WHEN ar.is_correct = 0 THEN 1 ELSE 0 END) as wrong_count,
                    ROUND(SUM(CASE WHEN ar.is_correct = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as wrong_rate
                FROM problems p
                JOIN answer_records ar ON p.problem_id = ar.problem_id
                GROUP BY p.problem_id
                ORDER BY wrong_rate DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def get_wrong_problems_by_user(self, user_id: int, limit: int = 10) -> List[sqlite3.Row]:
        """获取用户错题统计"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.problem_id,
                    p.operand1,
                    p.operation,
                    p.operand2,
                    p.answer,
                    COUNT(*) as wrong_count
                FROM problems p
                JOIN answer_records ar ON p.problem_id = ar.problem_id
                JOIN practice_records pr ON ar.record_id = pr.record_id
                WHERE pr.user_id = ? AND ar.is_correct = 0
                GROUP BY p.problem_id
                ORDER BY wrong_count DESC
                LIMIT ?
            ''', (user_id, limit))
            return cursor.fetchall()

# 初始化数据库连接
db_manager = DatabaseManager()

# 创建DAO实例
user_dao = UserDAO(db_manager)
class_dao = ClassDAO(db_manager)
problem_set_dao = ProblemSetDAO(db_manager)
problem_dao = ProblemDAO(db_manager)
practice_record_dao = PracticeRecordDAO(db_manager)
answer_record_dao = AnswerRecordDAO(db_manager)

def init_db():
    """初始化数据库"""
    db_manager.init_database()

if __name__ == '__main__':
    # 初始化数据库
    init_db()
    
    # 创建测试数据
    print("创建测试用户...")
    
    # 创建老师
    try:
        teacher_id = user_dao.create_user('teacher1', 'teacher_pass', 'teacher', '张老师')
        print(f"创建老师成功: {teacher_id}")
    except sqlite3.IntegrityError:
        print("老师已存在")
    
    # 创建班级
    try:
        class_id = class_dao.create_class('三年级一班', teacher_id, '三年级')
        print(f"创建班级成功: {class_id}")
    except sqlite3.IntegrityError:
        print("班级已存在")
    
    # 创建家长
    try:
        parent_id = user_dao.create_user('parent1', 'parent_pass', 'parent', '华经理')
        print(f"创建家长成功: {parent_id}")
    except sqlite3.IntegrityError:
        print("家长已存在")
    
    # 创建学生
    try:
        student_id = user_dao.create_user('student1', 'student_pass', 'student', '小明', class_id)
        print(f"创建学生成功: {student_id}")
    except sqlite3.IntegrityError:
        print("学生已存在")
    
    print("数据库初始化完成！")