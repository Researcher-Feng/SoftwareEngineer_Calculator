import unittest
from old.main2 import generate_expression_dp


class TestGenerateExpressionDP(unittest.TestCase):
    def test_empty_numbers(self):
        numbers = []
        operators = ["+", "-"]
        start = 0
        end = 1
        dp = {}
        op_count = 1
        max_gen = 10
        result = generate_expression_dp(numbers, operators, start, end, dp, op_count, max_gen)
        self.assertEqual(result, [])

    def test_empty_operators(self):
        numbers = [1, 2, 3]
        operators = []
        start = 0
        end = 2
        dp = {}
        op_count = 1
        max_gen = 10
        result = generate_expression_dp(numbers, operators, start, end, dp, op_count, max_gen)
        self.assertEqual(result, ["1", "2", "3"])

    def test_start_greater_than_end(self):
        numbers = [1, 2, 3]
        operators = ["+"]
        start = 2
        end = 1
        dp = {}
        op_count = 1
        max_gen = 10
        result = generate_expression_dp(numbers, operators, start, end, dp, op_count, max_gen)
        self.assertEqual(result, [])

    def test_max_gen_is_zero(self):
        numbers = [1, 2, 3]
        operators = ["+", "-"]
        start = 0
        end = 2
        dp = {}
        op_count = 1
        max_gen = 0
        result = generate_expression_dp(numbers, operators, start, end, dp, op_count, max_gen)
        self.assertEqual(result, [])