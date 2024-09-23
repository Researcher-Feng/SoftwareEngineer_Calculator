import itertools
import math


# 计算n个数能生成的最大不同表达式数
def count_unique_expressions(n):
    if n < 2:
        return 0  # 如果数字少于2个，不能生成有效的算式

    # 运算符
    all_operators = ['+', '-', '*', '÷']

    # 处理交换律的影响: + 和 * 的组合会引入重复
    unique_operator_combinations = set()
    for ops in itertools.product(all_operators, repeat=min(3, n - 1)):
        # 对可交换的运算符 ('+', '*') 排序，使其被认为是相同的表达式
        sorted_ops = tuple(sorted(ops, key=lambda x: (x == '+' or x == '*')))
        unique_operator_combinations.add(sorted_ops)

    unique_operator_count = len(unique_operator_combinations)

    # 根据n的不同情况计算可能的表达式数量
    if n == 2:
        # 当有2个数字时，只能有1个运算符
        num_permutations = math.perm(n, 2)  # 两个数字的排列
        operator_combinations = len(all_operators)  # 只能有1个运算符
        total_expressions = num_permutations * operator_combinations
    elif n == 3:
        # 当有3个数字时，可以有最多2个运算符
        num_permutations = math.perm(n, 3)  # 三个数字的排列
        operator_combinations = 4 ** 2  # 每个位置有2个运算符
        total_expressions = num_permutations * operator_combinations
    else:
        # 当有4个或更多数字时，可以有最多3个运算符
        num_permutations = math.perm(n, 4)  # 四个数字的排列
        total_expressions = num_permutations * unique_operator_count

    return total_expressions


# 示例：n = 6 时计算不同的表达式数
quick_dict = {}
for n in range(10):
    t_count = count_unique_expressions(n)
    n_count = int(t_count / 4 * 3)
    print(f"使用 {n} 个不同的数字，最多可以生成 {n_count} 个不同的算式。")
    quick_dict[n] = n_count
print(quick_dict)
