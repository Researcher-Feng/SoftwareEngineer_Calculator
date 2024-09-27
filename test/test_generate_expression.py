import unittest
import random
from main import generate_expression, evaluate_expression  # Replace with the actual module name


class TestGenerateExpression(unittest.TestCase):
    def setUp(self):
        self.r = 10  # 范围设置
        self.iterations = 100  # 设置测试迭代次数

    def test_generate_expression_basic(self):
        for _ in range(self.iterations):
            expression = generate_expression(self.r)
            if expression == -1:
                continue

            # 检查表达式是否包含数字或分数
            self.assertTrue(any(char.isdigit() for char in expression))
            self.assertTrue(any(char in ['/', ' ', '(', ')'] for char in expression))


    def test_generate_expression_format(self):
        for _ in range(self.iterations):
            expression = generate_expression(self.r)
            if expression == -1:
                continue

            # 检查表达式的格式
            self.assertIsInstance(expression, str)
            self.assertTrue(len(expression) > 0)


if __name__ == '__main__':
    unittest.main()