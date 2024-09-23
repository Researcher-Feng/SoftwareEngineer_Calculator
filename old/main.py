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


# 生成按钮回调函数
def on_generate():
    try:
        n = int(entry_num.get())
        r = int(entry_range.get())
        if n <= 0 or r <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的正整数。")
        return

    exercises, answers = generate_exercises(n, r)
    with open("Exercises.txt", 'w') as ef, open("Answers.txt", 'w') as af:
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成，结果已保存到Exercises.txt和Answers.txt。")


# 打开文件
def open_file_dialog():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return filename


# 判题按钮回调函数
def on_grade():
    exercise_file = open_file_dialog()
    answer_file = open_file_dialog()
    if not exercise_file or not answer_file:
        messagebox.showerror("文件错误", "请选择有效的题目文件和答案文件。")
        return

    with open(exercise_file, 'r') as ef, open(answer_file, 'r') as af:
        exercises = ef.readlines()
        answers = af.readlines()

    correct = []
    wrong = []
    invalid = []  # 用于存储无效的题目编号
    for i, (e, a) in enumerate(zip(exercises, answers), 1):
        expr = e.split('=')[0].strip()

        # 检查题目是否合法
        if not is_valid_expression(expr):
            invalid.append(i)
            continue  # 跳过这道题的批改

        # 如果题目有效，继续判题
        if evaluate_expression(expr) == Fraction(a):
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w') as gf:
        gf.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        gf.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
        if invalid:
            gf.write(f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})\n")

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"判题结果:\nCorrect: {len(correct)} ({', '.join(map(str, correct))})\n")
    result_text.insert(tk.END, f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
    if invalid:
        result_text.insert(tk.END, f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})\n")
    messagebox.showinfo("判题结果", "判题完成，结果已保存到Grade.txt")


# 创建主界面
root = tk.Tk()
root.title("四则运算题目生成器")

# 生成题目的设置
frame_generate = tk.Frame(root)
frame_generate.pack(pady=10)

label_num = tk.Label(frame_generate, text="题目数量:")
label_num.grid(row=0, column=0, padx=5, pady=5)
entry_num = tk.Entry(frame_generate)
entry_num.grid(row=0, column=1, padx=5, pady=5)

label_range = tk.Label(frame_generate, text="数值上届:")
label_range.grid(row=1, column=0, padx=5, pady=5)
entry_range = tk.Entry(frame_generate)
entry_range.grid(row=1, column=1, padx=5, pady=5)

button_generate = tk.Button(frame_generate, text="生成题目", command=on_generate)
button_generate.grid(row=2, columnspan=2, padx=5, pady=5)

# 判题功能
frame_grade = tk.Frame(root)
frame_grade.pack(pady=10)

button_grade = tk.Button(frame_grade, text="判题", command=on_grade)
button_grade.pack()

# 显示结果
result_text = tk.Text(root, height=15, width=50)
result_text.pack(padx=10, pady=10)

# 运行主循环
root.mainloop()
