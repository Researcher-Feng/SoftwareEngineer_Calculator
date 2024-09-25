import unittest
from main import generate_expression
import random

class TestEvalExpr(unittest.TestCase):
    def test_generate_expression_r1(self):
        expression = generate_expression(1)
        assert expression in ["1", "(1)"]

    def test_generate_expression_r2(self):
        expression = generate_expression(2)
        assert "÷" not in expression
        assert "1" not in expression
        assert ")" not in expression
        assert "+" in expression
        assert "-" in expression
        assert "*" in expression

    def test_generate_expression_r3(self):
        expression = generate_expression(3)
        assert "÷" in expression
        assert "1" in expression
        assert ")" in expression