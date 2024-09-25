import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
from fractions import Fraction
import re
from line_profiler_pycharm import profile


# 生成表达式
@profile
def generate_expression(r):
    # 生成一个数字
    def generate_number():
        # 为分数加上括号，确保计算时优先级正确
        if random.choice([True, False]):
            return str(random.randint(1, r))
        else:
            numerator = random.randint(1, r)
            # denominator = random.randint(2, r)
            # return f"({numerator}/{denominator})"  # 用括号包裹分数

            # 定义运算符列表
            denominator = random.randint(2, r)
            return f"({numerator}/{denominator})"  # 用括号包裹分数

    # 生成一个运算符
    ops = ['+', '-', '*', '÷']  # 除法运算使用 ÷ 号

    # 定义一个表达式字符串
    expression = generate_number()
    for _ in range(random.randint(1, 3)):  # 最多3个运算符
        op = random.choice(ops)
        next_num = generate_number()
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
        else:
            expression += f" {op} {next_num}"
    return expression


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
@profile
def is_valid_expression(expr):
    # 定义一个有效的表达式模式
    valid_pattern = r"^[\d\s\+\-\*÷/\(\)']+$"

    # 如果给定的表达式不符合模式，则返回 False
    if not re.match(valid_pattern, expr):
        return False

    if expr.count('(') != expr.count(')'):
        return False

    try:
        # 尝试将给定的表达式评估为一个数值
        result = evaluate_expression(expr)
        # 如果评估失败，则返回 False
        if result is None:
            return False
    except ZeroDivisionError:
        # 如果出现了除以零错误，则返回 False
        return False

    return True


# 生成题目和答案
@profile
def generate_exercises(n, r):
    exercises = [] # 定义一个列表，用于存储生成的练习题
    answers = [] # 定义一个列表，用于存储答案
    seen_expressions = set()  # 防止重复

    # 创建 Tkinter 窗口
    answer_set = set()

    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.title("加载中...")
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)
    progress['value'] = 0
    progress['maximum'] = n

    # 开始生成练习题和答案
    while len(exercises) < n:

        root.update()
        # 生成一个随机的算式
        expr = generate_expression(r)
        # 计算该算式的值
        answer = evaluate_expression(expr)
        # 如果答案不为 None，并且答案不在答案集中，则将答案添加到答案集中
        if n < 1000:
            if answer in answer_set:
                continue
            answer_set.add(answer)
        progress['value'] += 1
        # 如果答案不为 None，则将该算式和答案添加到练习题和答案列表中
        if answer is not None:
            normalized_expr = expr.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(expr + " = ")
                answers.append(str(answer))  # 用分数输出答案
                seen_expressions.add(normalized_expr)
    progress['value'] = n
    root.destroy()  # 关闭窗口
    return exercises, answers


# 生成按钮回调函数
@profile
def on_generate():
    try:
        # 从输入框中读取n和r的值
        n = int(entry_num.get())
        r = int(entry_range.get())
        # 判断输入是否有效
        if n <= 0 or r >= 10 or r <= 0:
            raise ValueError
    except ValueError:
        # 如果输入不合法，弹出错误提示
        messagebox.showerror("输入错误", "请输入10以内有效的正整数。")
        return

    # 生成n个包含r个选择项的选择题和答案
    exercises, answers = generate_exercises(n, r)
    # 使用with语句打开两个文件，分别用于保存题目和答案
    with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
        # 向两个文件中写入题目和答案
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    # 在文本框中显示生成的题目和答案
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
    # 打开选择题目文件对话框，并获取题目文件名
    exercise_file = open_file_dialog('选择题目文件')
    # 打开选择答案文件对话框，并获取答案文件名
    answer_file = open_file_dialog('选择答案文件')
    # 如果题目文件名或答案文件名为空，则弹出错误消息框
    if not exercise_file or not answer_file:
        messagebox.showerror("文件错误", "请选择有效的题目文件和答案文件。")
        return
    # 打开题目文件，读取题目和答案
    with open(exercise_file, 'r', encoding='utf-8') as ef, open(answer_file, 'r', encoding='utf-8') as af:
        exercises = ef.readlines()
        answers = af.readlines()
    # 定义一个列表，用于存储正确的题目序号
    correct = []
    # 定义一个列表，用于存储错误的题目序号
    wrong = []
    # 定义一个列表，用于存储无效的题目序号
    invalid = []  # 用于存储无效的题目编号
    # 遍历题目和答案，进行判题
    for i, (e, a) in enumerate(zip(exercises, answers), 1):
        # 分离出等式中的变量
        expr = e.split('=')[0].strip()

        # 检查题目是否合法
        if not is_valid_expression(expr):
            # 如果题目有效，继续判题
            invalid.append(i)
            continue  # 跳过这道题的批改

        # 如果题目有效，继续判题
        if str(evaluate_expression(expr)) == a.strip():
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w', encoding='utf-8') as gf:
        # 向 Grade.txt 文件中写入判题结果
        gf.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        gf.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
        if invalid:
            gf.write(f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})\n")

    # 显示判题结果的函数
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
