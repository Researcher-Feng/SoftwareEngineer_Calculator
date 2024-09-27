import time
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

# Convert mixed number to fraction
def convert_mixed_to_fraction(expr):
    # Regular expression to match mixed numbers
    mixed_pattern = r'(\d+)\'(\d+)/(\d+)'

    def replace_func(match):
        whole = int(match.group(1))
        numerator = int(match.group(2))
        denominator = int(match.group(3))
        # Calculate and return the corresponding fraction
        return str(Fraction(whole * denominator + numerator, denominator))

    # Replace mixed numbers with fractions
    return re.sub(mixed_pattern, replace_func, expr)


# Convert fraction to mixed number
def convert_fraction_to_mixed(fraction_str):
    """Convert a string representation of a fraction to a mixed number."""
    # Handle improper input
    if '/' not in fraction_str:
        return fraction_str  # If it's not a fraction, return as is

    # Split the fraction string into numerator and denominator
    try:
        numerator, denominator = map(int, fraction_str.split('/'))
    except ValueError:
        return None  # Handle non-integer values

    if denominator == 0:
        return None  # Handle the case of denominator being zero

    whole = numerator // denominator
    remainder = abs(numerator) % denominator  # Use abs to handle negative numerators

    if whole == 0:
        return f"{remainder}/{denominator}"  # Proper fraction
    elif remainder == 0:
        return str(whole)  # Whole number
    else:
        return f"{whole}'{remainder}/{denominator}"  # Mixed number



# 生成表达式
@profile
def generate_expression(r):
    def generate_number():
        if random.choice([True, False]):
            return str(random.randint(1, r-1))
        else:
            numerator = random.randint(1, r-1)
            denominator = random.randint(1, r-1)
            return convert_fraction_to_mixed(f"{numerator}/{denominator}")
            # return f"{numerator}/{denominator}"

    ops = ['+', '-', '×', '÷']
    expression = generate_number()
    added_parentheses = False  # Flag indicating whether parentheses have been added

    for _ in range(random.randint(1, 3)):
        op = random.choice(ops)
        next_num = generate_number()
        if random.choice([True, False]):
            expression = f"({expression} {op} {next_num})"
            added_parentheses = True  # Set flag to True
            if op == '-':
                if evaluate_expression(expression) < 0:
                    return -1
        else:
            expression += f" {op} {next_num}"
            added_parentheses = False  # Keep flag as False if no parentheses are added

    # Remove only the outermost parentheses
    if added_parentheses and expression.startswith('(') and expression.endswith(')'):
        expression = expression[1:-1]

    return expression



# Evaluate expression
@profile
def evaluate_expression(expr):
    try:
        expr = convert_mixed_to_fraction(expr)  # Convert mixed numbers to fractions
        expr = re.sub(r'(\d+)/(\d+)', r'(\1/\2)', expr) # put the fraction in parentheses to avoid the error
        expr = expr.replace("÷", "/")   # Replace division symbol with slash
        expr = expr.replace("×", "*")   # Replace times symbol with asterisk
        return eval_expr(expr)
    except ZeroDivisionError:
        return None
    except Exception:
        return None


@profile
def eval_expr(expr):
    expr = expr.replace(" ", "")
    expr = re.sub(r'(\d+)', r'Fraction("\1")', expr)
    expr = re.sub(r'\((\d+)/(\d+)\)', r'Fraction("\1", "\2")', expr)    # Replace with Fraction type
    try:
        result = eval(expr, {"__builtins__": None}, {"Fraction": Fraction})
        return result
    except ZeroDivisionError:
        return None


@profile
def is_valid_expression(expr):
    valid_pattern = r"^[\d\s\+\-\×÷/\(\)']+$"
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
def generate_exercises(n, r, bar=False):
    exercises = []
    answers = []
    seen_expressions = set()
    answer_set = set()
    progress = None
    root = None

    if bar:
        # 创建 Tkinter 窗口
        root = tk.Tk()
        root.title("加载中...")
        progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=20)
        progress['value'] = 0
        progress['maximum'] = n

    while len(exercises) < n:
        expr = generate_expression(r)
        if expr == -1:
            continue
        answer = evaluate_expression(expr)

        if answer < 0:
            continue
        answer = convert_fraction_to_mixed(str(answer))
        if answer in answer_set:
            continue
        answer_set.add(answer)


        if answer is not None:
            normalized_expr = expr.replace(" ", "")
            if normalized_expr not in seen_expressions:
                exercises.append(expr + " = ")
                answers.append(str(answer))
                seen_expressions.add(normalized_expr)
                if bar:
                    progress['value'] += 1  # 更新进度条
                    root.update()  # 更新窗口以反映进度条变化
    if bar:
        progress['value'] = n
        time.sleep(0.002)
        root.destroy()  # 关闭窗口

    return exercises, answers


# 生成题目的界面
@profile
def on_generate():
    try:
        n = int(entry_num.get())
        r = int(entry_range.get())
        if n <= 0 or r > 10 or r <= 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("输入错误", "[题目数量]请输入正整数；[数值上界]请输入大于1、小于等于10的正整数。")
        return

    exercises, answers = generate_exercises(n, r, bar=True)

    # Adding numbering to exercises and answers
    numbered_exercises = [f"{i + 1}. {exercise}" for i, exercise in enumerate(exercises)]
    numbered_answers = [f"{i + 1}. {answer}" for i, answer in enumerate(answers)]

    with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
        ef.write("\n".join(numbered_exercises))
        af.write("\n".join(numbered_answers))

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "生成题目:\n" + "\n".join(exercises))
    messagebox.showinfo("成功", "题目和答案已生成，结果已保存到 Exercises.txt 和 Answers.txt")



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
        # Remove the numbering from exercises and answers
        expr = e.split('.', 1)[-1].split('=')[0].strip()  # Get expression without the number
        answer = a.split('.', 1)[-1].strip()  # Get answer without the number

        if not is_valid_expression(expr):
            invalid.append(i)
            continue

        if str(evaluate_expression(expr)) == convert_mixed_to_fraction(answer):
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
    result_text.insert(tk.END, f"判题结果:\nCorrect: {len(correct)} ({', '.join(map(str, correct))})\n")
    result_text.insert(tk.END, f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
    if invalid:
        result_text.insert(tk.END, f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})\n")
    messagebox.showinfo("判题结果", "判题完成，结果已保存到 Grade.txt。")


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
          "                    要求 [生成的表达式数量] 为正整数，[数值上界] 为 大于1、小于10的正整数\n"
          "- 『答案校对』功能: 命令行输入 python main.py -e [题目路径] -a [答案路径]\n"
          "                    要求 [题目路径]、[答案路径] 均为对应 .txt 文件的绝对路径")


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
        logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
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
                if number <= 0:
                    logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
                    return
            except:
                logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
                sys.exit()
            if n_existed == 0:
                n_existed = 1
        elif opt in ("-r", "--ranging"):
            try:
                ranging = int(arg)
                if ranging > 10 or ranging <= 1:
                    logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
                    return
            except:
                logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
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
        logger.error("选项的参数输入有误，请重新输入。\n输入以下命令可以获得帮助：python main.py -h")
        sys.exit()

    # 执行生成四则运算题目功能
    if n_existed and r_existed:
        exercises, answers = generate_exercises(number, ranging)
        with open("Exercises.txt", 'w', encoding='utf-8') as ef, open("Answers.txt", 'w', encoding='utf-8') as af:
            ef.write("\n".join(exercises))
            af.write("\n".join(answers))
        logger.info("\n已随机生成四则运算题目与对应答案，分别存入当前目录下的 Exercises.txt 文件和 Answers.txt 文件")

    # 执行判定答案对错功能
    if e_existed and a_existed:
        correct, wrong, invalid = judge_function(exercise_file, answer_file)
        print(f"判题结果:\nCorrect: {len(correct)} ({', '.join(map(str, correct))})")
        print(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})")
        if invalid:
            print(f"Invalid: {len(invalid)} ({', '.join(map(str, invalid))})")
        logger.info("\n判题完成，结果已保存到当前目录下的 Grade.txt")

    sys.exit()


if __name__ == "__main__":
    logger = color_logger()
    if len(sys.argv) > 1:
        handle_cli_args()
    else:
        setup_gui()

