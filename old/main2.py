import tkinter as tk
from tkinter import filedialog, messagebox
import random
from fractions import Fraction
import re
from line_profiler_pycharm import profile
from jupyter_client.session import msg_header

ops = ['+', '-', '*', '÷']   # 运算符
quick_dict = {0: 0, 1: 0, 2: 6, 3: 72, 4: 576, 5: 2880, 6: 8640, 7: 20160, 8: 40320, 9: 72576}
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
    if op_count < 3:
        # 递归的前提是运算符的数量没有超过3
        for i in range(start, end):
            left_exprs = generate_expression_dp(numbers, operators, start, i, dp, op_count, max_gen)
            if left_exprs == -1:
                return -1
            # right_exprs = generate_expression_dp(numbers, operators, i + 1, end, dp, op_count + len(left_exprs) - 1,
            right_exprs = generate_expression_dp(numbers, operators, i + 1, end, dp, op_count + len(left_exprs),
                                                 max_gen)
            if right_exprs == -1:
                return -1
            for left in left_exprs:
                for right in right_exprs:
                    for op in operators:
                        # 只在运算符数量小于3的情况下生成表达式
                        if op_count < 3:
                            new_expr = f"({left} {op} {right})"
                            result.append(new_expr)
                            gen_result.append(new_expr)
                            if len(gen_result) >= max_gen:
                                gen_result = gen_result[:max_gen]
                                return -1
    # if op_count < 3:
    #     for i in range(start, end):
    #         left_exprs = generate_expression_dp(numbers, operators, start, i, dp, op_count, max_gen)
    #         if left_exprs == -1:
    #             return -1
    #         right_exprs = generate_expression_dp(numbers, operators, i + 1, end, dp, op_count, max_gen)
    #         if right_exprs == -1:
    #             return -1
    #         for left in left_exprs:
    #             for right in right_exprs:
    #                 for op in operators:
    #                     result.append(f"({left} {op} {right})")
    #                     gen_result.append(f"({left} {op} {right})")
    #                     if len(gen_result) >= max_gen:
    #                         gen_result = gen_result[:max_gen]
    #                         return -1

    dp[(start, end, op_count)] = result
    return result


# 修改后的生成表达式函数
def generate_unique_expressions_dp(r, count=5):
    global ops
    global gen_result
    numbers = list(range(1, r+1))
    expression_set = set()
    dp = {}
    count = limit_judge(r, count)

    if r == 2:
        # 当只有2个数字时，生成4个不同的表达式
        a, b = numbers
        expressions = [f"{a} {op} {b}" for op in ops]
        random.seed()
        random.shuffle(expressions)
        expressions += [f"{b} {op} {a}" for op in ops if op in ['-', '÷']]  # 处理非交换律运算符
        random.shuffle(expressions)
        gen_result.extend(expressions)
        return set(expressions[:count])  # 限制生成的数量

    while len(expression_set) < count:
        random.seed()
        random.shuffle(numbers)
        random.shuffle(ops)
        expr_list = generate_expression_dp(numbers, ops, 0, len(numbers) - 1, dp, 0, count)
        if expr_list == -1:
            for i_gen in gen_result:
                expression_set.add(i_gen)
    return expression_set


# 判断输入的数字是否超出了预先生成的限制
def limit_judge(r, count):
    # 首先从quick_dict字典中获取到当前字符的限制数量
    limit = quick_dict[r]
    # 如果输入的数字数量大于限制数量，则警告
    if count > limit:
        limit_error(r, limit)
        return limit
    # 否则，返回输入的数字数量
    else:
        return count


def limit_error(r, limit):
    messagebox.showerror("输入错误",
                         f"使用 {r} 个不同的数字，最多只可以生成 {limit} 个不同的算式。下面生成能力范围内的算式。")


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
@profile
def generate_exercises(n, r):
    global gen_result
    exercises = []
    answers = []
    seen_expressions = set()  # 防止重复

    gen_result.clear()
    expr_t = generate_unique_expressions_dp(r, n)
    for i_t in expr_t:
        answer = evaluate_expression(i_t)
        if answer is not None:
            normalized_expr = i_t.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(i_t + " = ")
                answers.append(str(answer))  # 用分数输出答案
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
    with open("../Exercises.txt", 'w', encoding='utf-8') as ef, open("../Answers.txt", 'w', encoding='utf-8') as af:
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成。")


# 打开文件
def open_file_dialog(msg_string):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], title=msg_string)
    return filename


# 判题按钮回调函数
def on_grade():
    exercise_file = open_file_dialog('选择题目文件')
    answer_file = open_file_dialog('选择答案文件')
    if not exercise_file or not answer_file:
        messagebox.showerror("文件错误", "请选择有效的题目文件和答案文件。")
        return
    with open(exercise_file, 'r', encoding='utf-8') as ef, open(answer_file, 'r', encoding='utf-8') as af:
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

    with open('../Grade.txt', 'w') as gf:
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

label_range = tk.Label(frame_generate, text="最大数值:")
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
