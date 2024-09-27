import unittest
import random
from main import generate_expression, evaluate_expression


class TestGenerateExpression(unittest.TestCase):
    def setUp(self):
        self.r = 10  # Set the range
        self.iterations = 100  # Set the number of test iterations

    def test_generate_expression_basic(self):
        for _ in range(self.iterations):
            expression = generate_expression(self.r)
            if expression == -1:
                continue

            # Check if the expression contains numbers or fractions
            self.assertTrue(any(char.isdigit() for char in expression))
            self.assertTrue(any(char in ['/', ' ', '(', ')'] for char in expression))


    def test_generate_expression_format(self):
        for _ in range(self.iterations):
            expression = generate_expression(self.r)
            if expression == -1:
                continue

            # Check the format of the expression
            self.assertIsInstance(expression, str)
            self.assertTrue(len(expression) > 0)


if __name__ == '__main__':
    unittest.main()
