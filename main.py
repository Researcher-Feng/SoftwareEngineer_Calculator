import tkinter as tk
from tkinter import filedialog, messagebox
import random
from fractions import Fraction
import re


# 生成表达式
def generate_expression(r):
    def generate_number():
        if random.choice([True, False]):
            return str(random.randint(1, r - 1))
        else:
            numerator = random.randint(1, r - 1)
            denominator = random.randint(2, r - 1)
            return f"{numerator}/{denominator}"

    ops = ['+', '-', '*', '/']
    expression = generate_number()
    for _ in range(random.randint(1, 3)):  # 最多3个运算符
        op = random.choice(ops)
        next_num = generate_number()
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
        else:
            expression += f" {op} {next_num}"
    return expression


# 计算表达式并返回分数
def evaluate_expression(expr):
    try:
        # 用Fraction来计算结果，避免浮点数运算
        return Fraction(eval(expr.replace("/", " / "), {"__builtins__": None}, {"Fraction": Fraction}))
    except ZeroDivisionError:
        return None
    except Exception:
        return None


# 检查题目格式和合法性
def is_valid_expression(expr):
    # 正则表达式匹配合法的自然数、真分数、运算符、括号
    valid_pattern = r"^[\d\s\+\-\*/\(\)']+$"

    # 检查格式是否符合
    if not re.match(valid_pattern, expr):
        return False

    # 检查括号配对是否正确
    if expr.count('(') != expr.count(')'):
        return False

    # 检查除以零的情况
    try:
        result = evaluate_expression(expr)
        if result is None:
            return False
    except ZeroDivisionError:
        return False

    return True


# 生成题目和答案
def generate_exercises(n, r):
    exercises = []
    answers = []
    seen_expressions = set()  # 防止重复
    while len(exercises) < n:
        expr = generate_expression(r)
        answer = evaluate_expression(expr.replace("/", " / "))
        if answer is not None and answer >= 0:
            normalized_expr = expr.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(expr + " = ")
                answers.append(str(answer))  # 直接用分数形式输出答案
                seen_expressions.add(normalized_expr)
    return exercises, answers





# 打开文件
def open_file_dialog():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return filename





