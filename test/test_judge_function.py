import unittest
import os
from main import judge_function, is_valid_expression, evaluate_expression, convert_mixed_to_fraction

class TestJudgeFunction(unittest.TestCase):
    def setUp(self):
        # 创建临时的输入文件
        self.exercise_file = 'test_exercises.txt'
        self.answer_file = 'test_answers.txt'
        self.grade_file = 'Grade.txt'

        with open(self.exercise_file, 'w', encoding='utf-8') as ef:
            ef.write("1. 3 + 5 =\n")
            ef.write("2. 10 - 2 =\n")
            ef.write("3. 6 ÷ 0 =\n")
            ef.write("4. 8 × 2 =\n")
            ef.write("5. 1/2 + 1/2 =\n")

        with open(self.answer_file, 'w', encoding='utf-8') as af:
            af.write("1. 8\n")
            af.write("2. 8\n")
            af.write("3. undefined\n")  # Invalid case
            af.write("4. 16\n")
            af.write("5. 1\n")

    def tearDown(self):
        # 删除临时文件
        os.remove(self.exercise_file)
        os.remove(self.answer_file)
        if os.path.exists(self.grade_file):
            os.remove(self.grade_file)

    def test_judge_function(self):
        correct, wrong, invalid = judge_function(self.exercise_file, self.answer_file)

        # 检查正确和错误的索引
        self.assertEqual(correct, [1, 2, 4, 5])  # 期望的正确答案索引
        self.assertEqual(wrong, [])  # 无错误
        self.assertEqual(invalid, [3])  # 包含无效答案的索引

    def test_invalid_expression(self):
        # 测试无效表达式
        with open(self.exercise_file, 'w', encoding='utf-8') as ef:
            ef.write("1. 3 + 5 =\n")
            ef.write("2. invalid_expression\n")  # 无效表达式

        with open(self.answer_file, 'w', encoding='utf-8') as af:
            af.write("1. 8\n")
            af.write("2. 0\n")  # 任意答案

        correct, wrong, invalid = judge_function(self.exercise_file, self.answer_file)

        self.assertEqual(invalid, [2])  # 确保无效表达式被记录

if __name__ == '__main__':
    unittest.main()
