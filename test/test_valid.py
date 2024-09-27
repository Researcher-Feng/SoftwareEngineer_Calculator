import unittest
from main import is_valid_expression


class TestIsValidExpression(unittest.TestCase):

    def test_valid_expressions(self):
        """Test if valid expressions return True"""
        valid_expressions = [
            "3 + 2",
            "4 - 1 + 1",
            "5 × 2",
            "(1/2 + 1/2)",
            "10 ÷ 2"
        ]

        for expr in valid_expressions:
            with self.subTest(expr=expr):
                self.assertTrue(is_valid_expression(expr))

    def test_invalid_expressions(self):
        """Test if invalid expressions return False"""
        invalid_expressions = [
            "2 + ",
            "3 ÷ 0",
            "(3 - 1",
            "× 5",
            "10 ÷ a",
            "3 + 5 ×",
            "3 ++ 5",
            "3 + (5 * 2"
        ]

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                self.assertFalse(is_valid_expression(expr))

    def test_empty_string(self):
        """Test if empty string returns False"""
        self.assertFalse(is_valid_expression(""))


if __name__ == '__main__':
    unittest.main()
