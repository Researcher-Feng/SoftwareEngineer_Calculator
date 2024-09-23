import tkinter as tk
from tkinter import filedialog, messagebox
import random
from fractions import Fraction
import re
ops = ['+', '-', '*', '÷']
gen_count = 0
gen_result = []


# 使用动态规划生成表达式，限制最多包含三个运算符
def generate_expression_dp(numbers, operators, start, end, dp, op_count, max_gen):
    global gen_count
    global gen_result
    if start == end:
        return [str(numbers[start])]

    if (start, end, op_count) in dp:
        return dp[(start, end, op_count)]

    result = []
    # 递归的前提是运算符的数量没有超过3
    if op_count < 3:
        for i in range(start, end):
            left_exprs = generate_expression_dp(numbers, operators, start, i, dp, op_count, max_gen)
            if left_exprs == -1:
                return -1
            right_exprs = generate_expression_dp(numbers, operators, i + 1, end, dp, op_count, max_gen)
            if right_exprs == -1:
                return -1
            for left in left_exprs:
                for right in right_exprs:
                    for op in operators:
                        result.append(f"({left} {op} {right})")
                        gen_result.append(f"({left} {op} {right})")
                        if len(gen_result) >= max_gen:
                            gen_result = gen_result[:max_gen]
                            return -1

    dp[(start, end, op_count)] = result
    return result

def generate_unique_expressions_dp(r, count=5):
    global ops
    global gen_result
    numbers = list(range(1, r))
    expression_set = set()
    dp = {}
    while len(expression_set) < count:
        random.shuffle(numbers)
        expr_list = generate_expression_dp(numbers, ops, 0, len(numbers) - 1, dp, 0, count)
        if expr_list == -1:
            for i_gen in gen_result:
                expression_set.add(i_gen)
    return expression_set


# 生成表达式
def generate_expression(r):
    global ops
    # 生成一个数字
    def generate_number():
        # 为分数加上括号，确保计算时优先级正确
        if random.choice([True, False]):
            return str(random.randint(1, r - 1))
        else:
            numerator = random.randint(1, r - 1)
            denominator = random.randint(2, r - 1)
            return f"({numerator}/{denominator})"  # 用括号包裹分数
    # 除法运算使用 ÷ 号
    # 生成一个数字
    expression = generate_number()
    # 最多生成三个运算符
    for _ in range(random.randint(1, 3)):  # 最多3个运算符
        op = random.choice(ops)
        # 生成一个数字
        next_num = generate_number()
        # 如果随机数为真，则将运算符放在数字前面
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
        else:
            expression += f" {op} {next_num}"
    return expression


# 手动解析和计算表达式，使用 Fraction 来保证分数精度
def evaluate_expression(expr):
    try:
        # 将 ÷ 替换为 / 并计算
        expr = expr.replace("÷", "/")
        return eval_expr(expr)
    except ZeroDivisionError:
        return None
    except Exception:
        return None


# 使用 Fraction 进行 eval 运算，避免使用浮点数
def eval_expr(expr):
    # 安全地用正则表达式提取出运算符和数值，并将数值转换为 Fraction
    expr = expr.replace(" ", "")
    expr = re.sub(r'(\d+)', r'Fraction("\1")', expr)  # 替换为 Fraction 类型
    expr = re.sub(r'\((\d+)/(\d+)\)', r'Fraction("\1", "\2")', expr)  # 真分数解析并加括号
    try:
        result = eval(expr, {"__builtins__": None}, {"Fraction": Fraction})
        return result
    except ZeroDivisionError:
        return None


# 检查题目格式和合法性
def is_valid_expression(expr):
    valid_pattern = r"^[\d\s\+\-\*÷/\(\)']+$"

    if not re.match(valid_pattern, expr):
        return False

    if expr.count('(') != expr.count(')'):
        return False

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

    expr_t = generate_unique_expressions_dp(r, n)
    for i_t in expr_t:
        answer = evaluate_expression(i_t)
        if answer is not None:
            normalized_expr = i_t.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(i_t + " = ")
                answers.append(str(answer))  # 用分数输出答案
                seen_expressions.add(normalized_expr)

    # while len(exercises) < n:
    #     expr = generate_expression(r)
    #     answer = evaluate_expression(expr)
    #     if answer is not None:
    #         normalized_expr = expr.replace(" ", "")
    #         if normalized_expr not in seen_expressions:
    #             exercises.append(expr + " = ")
    #             answers.append(str(answer))  # 用分数输出答案
    #             seen_expressions.add(normalized_expr)
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
    with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成。")


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
        if str(evaluate_expression(expr)) == a.strip():
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
    messagebox.showinfo("判题结果", "判题完成，结果已保存到Grade.txt。")


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

label_range = tk.Label(frame_generate, text="数值范围:")
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
