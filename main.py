import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
from fractions import Fraction
import getopt
import re
from line_profiler_pycharm import profile
import sys
import logging
import colorlog
logger = None


@profile
# 彩色日志
def color_logger():
    log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    logger = logging.getLogger('logger_name')
    # 输出到控制台
    console_handler = logging.StreamHandler()
    # 输出到文件
    file_handler = logging.FileHandler(filename='test.log', mode='a', encoding='utf8')

    # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
    logger.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)

    # 日志输出格式
    file_formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S'
    )
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # 重复日志问题：
    # 1、防止多次addHandler；
    # 2、loggername 保证每次添加的时候不一样；
    # 3、显示完log之后调用removeHandler
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    console_handler.close()
    file_handler.close()
    return logger


@profile
# GUI 图形化界面
def setup_gui():
    root = tk.Tk()
    root.title("四则运算题目生成器")

    # Generate problem settings
    frame_generate = tk.Frame(root)
    frame_generate.pack(pady=10)

    label_num = tk.Label(frame_generate, text="题目数量:")
    label_num.grid(row=0, column=0, padx=5, pady=5)
    global entry_num
    entry_num = tk.Entry(frame_generate)
    entry_num.grid(row=0, column=1, padx=5, pady=5)

    label_range = tk.Label(frame_generate, text="数值上届:")
    label_range.grid(row=1, column=0, padx=5, pady=5)
    global entry_range
    entry_range = tk.Entry(frame_generate)
    entry_range.grid(row=1, column=1, padx=5, pady=5)

    button_generate = tk.Button(frame_generate, text="生成题目", command=on_generate)
    button_generate.grid(row=2, columnspan=2, padx=5, pady=5)

    # Grading function
    frame_grade = tk.Frame(root)
    frame_grade.pack(pady=10)

    button_grade = tk.Button(frame_grade, text="判题", command=on_grade)
    button_grade.pack()

    # Display result
    global result_text
    result_text = tk.Text(root, height=15, width=50)
    result_text.pack(padx=10, pady=10)

    root.mainloop()


# 生成表达式
@profile
def generate_expression(r):
    def generate_number():
        if random.choice([True, False]):
            return str(random.randint(1, r))
        else:
            numerator = random.randint(1, r)
            denominator = random.randint(1, r)
            return f"({numerator}/{denominator})"

    ops = ['+', '-', '*', '÷']
    expression = generate_number()
    for _ in range(random.randint(1, 3)):
        op = random.choice(ops)
        next_num = generate_number()
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
        else:
            expression += f" {op} {next_num}"
    return expression


# Evaluate expression
@profile
def evaluate_expression(expr):
    try:
        expr = expr.replace("÷", "/")
        return eval_expr(expr)
    except ZeroDivisionError:
        return None
    except Exception:
        return None


@profile
def eval_expr(expr):
    expr = expr.replace(" ", "")
    expr = re.sub(r'(\d+)', r'Fraction("\1")', expr)
    expr = re.sub(r'\((\d+)/(\d+)\)', r'Fraction("\1", "\2")', expr)
    try:
        result = eval(expr, {"__builtins__": None}, {"Fraction": Fraction})
        return result
    except ZeroDivisionError:
        return None


@profile
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


@profile
def generate_exercises(n, r):
    exercises = []
    answers = []
    seen_expressions = set()
    answer_set = set()

    while len(exercises) < n:
        expr = generate_expression(r)
        answer = evaluate_expression(expr)
        if n < 1000:
            if answer in answer_set:
                continue
            answer_set.add(answer)

        if answer is not None:
            normalized_expr = expr.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(expr + " = ")
                answers.append(str(answer))
                seen_expressions.add(normalized_expr)
    return exercises, answers


# 生成题目的界面
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
    with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
        ef.write("\n".join(exercises))
        af.write("\n".join(answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成，结果已保存到Exercises.txt和Answers.txt。")


# Grading button callback
@profile
def judge_function(exercise_file, answer_file):
    with open(exercise_file, 'r', encoding='utf-8') as ef, open(answer_file, 'r', encoding='utf-8') as af:
        exercises = ef.readlines()
        answers = af.readlines()

    correct = []
    wrong = []
    invalid = []

    for i, (e, a) in enumerate(zip(exercises, answers), 1):
        expr = e.split('=')[0].strip()
        if not is_valid_expression(expr):
            invalid.append(i)
            continue

        if str(evaluate_expression(expr)) == a.strip():
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w', encoding='utf-8') as gf:
        gf.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        gf.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
        if invalid:
            gf.write(f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})\n")
    return correct, wrong, invalid


# 题目判定的界面
@profile
def on_grade():
    exercise_file = open_file_dialog('选择题目文件')
    answer_file = open_file_dialog('选择答案文件')
    if not exercise_file or not answer_file:
        messagebox.showerror("文件错误", "请选择有效的题目文件和答案文件。")
        return

    correct, wrong, invalid = judge_function(exercise_file, answer_file)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"判题结果:\n答案正确: {len(correct)} ({', '.join(map(str, correct))})\n")
    result_text.insert(tk.END, f"答案错误: {len(wrong)} ({', '.join(map(str, wrong))})\n")
    if invalid:
        result_text.insert(tk.END, f"答案无效: {len(invalid)} ({', '.join(map(str, invalid))})\n")
    messagebox.showinfo("判题结果", "判题完成，结果已保存到Grade.txt。")


# Open file dialog
@profile
def open_file_dialog(msg_string):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], title=msg_string)
    return filename


@profile
def help_msg():
    logger.warning("\n命令行方式使用须知"
          "该四则运算器拥有『题目生成』和『答案校对』两个功能，每次使用都需要提供合适的参数：\n"
          "- 『题目生成』功能: 命令行输入 python main.py -n [生成的表达式数量] -r [数值上届]\n"
          "                    要求 [生成的表达式数量] 为正整数，[数值上届] 为 10 以内正整数\n"
          "- 『答案校对』功能: 命令行输入 python main.py -e [题目路径] -a [答案路径]\n"
          "                    要求 [题目路径]、[答案路径] 均为对应 .txt 文件的绝对路径")
@profile
def wrong_msg():
    logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
@profile
def success_gen_msg():
    logger.info("\n已随机生成四则运算题目与对应答案，分别存入当前目录下的 Exercises.txt 文件和 Answers.txt 文件")
@profile
def success_judge_msg():
    logger.info("\n判题完成，结果已保存到当前目录下的 Grade.txt")




# 命令行模式-处理逻辑
@profile
def handle_cli_args():
    number = 0
    ranging = 0
    exercise_file = " "
    answer_file = " "
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:r:e:a:", ["help", "number=", "range=", "exercise_file=", "answer_file="])
    except:
        wrong_msg()
        help_msg()
        sys.exit()

    # 从左到右：是否包含生成题目数量、是否包含数值范围上届、是否包含题目路径、是否包含答案路径
    n_existed, r_existed, e_existed, a_existed = 0, 0, 0, 0
    for opt, arg in opts:
        if opt in ("-h", "--help"):  # 显示帮助
            help_msg()
            sys.exit()
        if opt in ("-n", "--number"):
            try:
                number = int(arg)
            except:
                wrong_msg()
                sys.exit()
            if n_existed == 0:
                n_existed = 1
        elif opt in ("-r", "--ranging"):
            try:
                ranging = int(arg)
            except:
                wrong_msg()
                sys.exit()
            if r_existed == 0:
                r_existed = 1
        elif opt in ("-e", "--exercise_file"):
            exercise_file = arg
            if e_existed == 0:
                e_existed = 1
        elif opt in ("-a", "--answer_file"):
            answer_file = arg
            if a_existed == 0:
                a_existed = 1
        else:
            help_msg()
            sys.exit()

    # 检测参数输入错误
    if (r_existed == 1 and n_existed == 0) or (r_existed == 0 and n_existed == 1) \
            or (e_existed == 1 and a_existed == 0) or (e_existed == 0 and a_existed == 1) or \
            (r_existed == 0 and n_existed == 0 and e_existed == 0 and a_existed == 0):
        wrong_msg()
        sys.exit()

    # 执行生成四则运算题目功能
    if n_existed and r_existed:
        exercises, answers = generate_exercises(number, ranging)
        with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
            ef.write("\n".join(exercises))
            af.write("\n".join(answers))
        success_gen_msg()

    # 执行判定答案对错功能
    if e_existed and a_existed:
        correct, wrong, invalid = judge_function(exercise_file, answer_file)
        print(f"判题结果:\n答案正确: {len(correct)} ({', '.join(map(str, correct))})")
        print(f"答案错误: {len(wrong)} ({', '.join(map(str, wrong))})")
        if invalid:
            print(f"答案无效: {len(invalid)} ({', '.join(map(str, invalid))})")
        success_judge_msg()

    sys.exit()


if __name__ == "__main__":
    logger = color_logger()
    if len(sys.argv) > 1:
        handle_cli_args()
    else:
        setup_gui()

