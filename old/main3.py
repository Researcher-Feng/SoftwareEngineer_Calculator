import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
from fractions import Fraction
import re
ops = ['+', '-', '*', '/']
ops_find = [' + ', ' - ', ' * ', ' / ']
from line_profiler_pycharm import profile


# 生成表达式
@profile
def generate_expression(r):
    global ops
    def generate_number():
        if random.choice([True, False]):
            return str(random.randint(1, r))
        else:
            numerator = random.randint(1, r)
            denominator = random.randint(2, r)
            return f"{numerator}/{denominator}"
    expression = generate_number()
    for _ in range(random.randint(1, 3)):  # 最多3个运算符
        op = random.choice(ops)
        next_num = generate_number()
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
        else:
            expression += f" {op} {next_num}"
    expression_list = []
    for i_op in ops_find:
        op_index = expression.find(i_op)
        if op_index != -1:
            for r_op in ops_find:
                r_expression = expression.replace(i_op, r_op)
                expression_list.append(r_expression)
    return expression_list


# 手动解析和计算表达式，使用 Fraction 来保证分数精度
@profile
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
@profile
def eval_expr(expr):
    if '/' in expr:
        expr = transform_string_format(expr)
    try:
        result = eval(expr, {"__builtins__": None}, {"Fraction": Fraction})
        return result
    except ZeroDivisionError:
        return None


def transform_string_format(expr):
    # 安全地用正则表达式提取出运算符和数值，并将数值转换为 Fraction
    expr = expr.replace(" ", "")  # 真分数解析并加括号
    expr = re.sub(r'(\d+)', r'Fraction("\1")', expr)  # 替换为 Fraction 类型
    expr = re.sub(r'\((\d+)/(\d+)\)', r'Fraction("\1", "\2")', expr)
    return expr


# 检查题目格式和合法性
@profile
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
@profile
def generate_exercises(n, r):
    exercises = []
    answers = []
    answer_set = set()

    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.title("加载中...")
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)
    progress['value'] = 0
    progress['maximum'] = n

    # 防止重复
    start_time = time.time()
    while len(answer_set) < n:

        progress['value'] += 4  # 更新进度条
        # time.sleep(0.002)
        root.update()  # 更新窗口以反映进度条变化

        current_time = time.time()
        if current_time - start_time >= 1200:
            raise_callback_msg()
            root.destroy()  # 关闭窗口
            return -1, -1
        expr_list = generate_expression(r)
        for expr in expr_list:
            answer = evaluate_expression(expr.replace("/", " / "))

            if n < 1000:
                if answer in answer_set:
                    progress['value'] -= 1
                    continue
            if answer is not None and answer >= 0:
                exercises.append(expr + " = ")
                answers.append(str(answer))  # 直接用分数形式输出答案
                answer_set.add(str(answer))
            else:
                progress['value'] -= 1
                continue

    progress['value'] = n
    root.destroy()  # 关闭窗口
    return exercises, answers


@profile
def raise_callback_msg():
    messagebox.showerror("输入错误", "无法生成足够的题目。请检查输入的题目数量与数值上届，并重新输入。")


# 生成按钮回调函数
@profile
def on_generate():
    try:
        n = int(entry_num.get())
        r = int(entry_range.get())
        if n <= 0 or r >= 10 or r <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("输入错误", "请输入10以内有效的正整数。")
        return

    exercises, answers = generate_exercises(n, r)
    if exercises == -1:
        return
    with open("Exercises.txt", 'w') as ef, open("Answers.txt", 'w') as af:
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成，结果已保存到Exercises.txt和Answers.txt。")


# 打开文件
@profile
def open_file_dialog(msg_string):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], title=msg_string)
    return filename


# 判题按钮回调函数
@profile
def on_grade():
    exercise_file = open_file_dialog('选择题目文件')
    answer_file = open_file_dialog('选择答案文件')
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
