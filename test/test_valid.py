import unittest
from main import is_valid_expression


class TestIsValidExpression(unittest.TestCase):
    def test_empty_string(self):
        self.assertFalse(is_valid_expression(""))

    def test_only_numbers(self):
        self.assertTrue(is_valid_expression("12345"))

    def test_only_operators(self):
        self.assertFalse(is_valid_expression("+ - * / ( )"))

    def test_division_or_zero(self):
        self.assertFalse(is_valid_expression("123 / 0"))
        self.assertFalse(is_valid_expression("123 / 456 * 789"))