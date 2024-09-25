import unittest
from main import eval_expr


class TestEvalExpr(unittest.TestCase):
    def test_empty_string(self):
        self.assertIsNone(eval_expr(""))

    def test_illegal_characters(self):
        self.assertIsNone(eval_expr("a+b"))

    def test_zero_divisor(self):
        self.assertIsNone(eval_expr("1/0"))

    def test_normal_case(self):
        self.assertEqual(eval_expr("1/3 + 2/5"), 5/15)