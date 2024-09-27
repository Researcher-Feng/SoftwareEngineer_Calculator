import unittest
import re
from main import evaluate_expression


class TestEvaluateExpression(unittest.TestCase):

    def test_valid_expressions(self):
        """Test if valid expressions evaluate correctly"""
        valid_expressions = [
            "3 + 5",
            "10 - 2 × 3",
            "8 ÷ 4 + 1",
            "1/2 + 1/2",
            "5 × (3 - 1)"
        ]

        expected_results = [
            8,  # 3 + 5
            4,  # 10 - 2 × 3
            3.0,  # 8 ÷ 4 + 1
            1.0,  # 1/2 + 1/2
            10  # 5 × (3 - 1)
        ]

        for expr, expected in zip(valid_expressions, expected_results):
            with self.subTest(expr=expr):
                self.assertEqual(evaluate_expression(expr), expected)

    def test_division_by_zero(self):
        """Test if division by zero returns None"""
        expr = "1 ÷ 0"
        self.assertIsNone(evaluate_expression(expr))

    def test_invalid_expressions(self):
        """Test if invalid expressions return None"""
        invalid_expressions = [
            "2 + ",
            "× 5",
            "10 ÷ a",
            "5 / (3 - 3)",
            "1/0 + 1",
            ""  # Test for empty string
        ]

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                self.assertIsNone(evaluate_expression(expr))


if __name__ == '__main__':
    unittest.main()
