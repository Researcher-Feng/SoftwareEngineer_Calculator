import unittest
from fractions import Fraction
from main import eval_expr  # Replace with the actual module name


class TestEvalExpr(unittest.TestCase):

    def test_valid_expressions(self):
        """Test if valid expressions evaluate correctly"""
        valid_expressions = [
            "3 + 2",
            "4 - 1 + 1",
            "5 * 2",
            "(1/2 + 1/2)",
            "10 / 2"
        ]

        expected_results = [
            5,  # 3 + 2
            4,  # 4 - 1 + 1
            10,  # 5 × 2
            1,  # 1/2 + 1/2
            5  # 10 ÷ 2
        ]

        for expr, expected in zip(valid_expressions, expected_results):
            with self.subTest(expr=expr):
                self.assertEqual(eval_expr(expr), expected)



    def test_fraction_expressions(self):
        """Test if fraction expressions evaluate correctly"""
        fraction_expressions = [
            "1/2 + 1/2",
            "1/3 + 2/3",
            "(1/4 + 3/4) * 2"
        ]

        expected_results = [
            1,  # 1/2 + 1/2
            1,  # 1/3 + 2/3
            2  # (1/4 + 3/4) × 2
        ]

        for expr, expected in zip(fraction_expressions, expected_results):
            with self.subTest(expr=expr):
                self.assertEqual(eval_expr(expr), expected)



if __name__ == '__main__':
    unittest.main()
