import unittest
from main import evaluate_expression


class TestEvaluateExpression(unittest.TestCase):
    def test_empty_string(self):
        self.assertIsNone(evaluate_expression(""))

    def test_division_by_zero(self):
        self.assertIsNone(evaluate_expression("1/0"))

    def test_invalid_syntax(self):
        self.assertIsNone(evaluate_expression("1 + 2 *"))