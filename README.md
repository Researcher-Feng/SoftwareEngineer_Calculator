## 软件工程-四则运算生成器



### 运行环境

以下是基本需求（更详细的环境需求请参考`requirements.txt`）：

- Python 3.9.13

### 项目结构

```
.
├── .idea
├── 3121005661
├── 3122004905
├── old						    // 存放旧的代码版本
│   ├── main1.py		
│   ├── main2.py
│   ├── main3.py
│   └── main4.py		
├── test						// 存放测试类
│   ├── graph.py	  // 代码调用关系图
│   ├── test.log	  // 空文件
│   ├── test_eval.py	  // 测试函数：字符串数学化
│   ├── test_evaluate.py	  // 测试函数：评估函数
│   ├── test_fraction_function.py	  // 测试函数：真分数字符串预处理
│   ├── test_generate_exercises.py		  // 测试函数：练习题生成
│   ├── test_generate_expression.py		  // 测试函数：表达式生成
│   ├── test_judge_function.py		  // 测试函数：答案校对
│   ├── test_logger.py		  // 测试函数：日志生成
│   └── test_valid.py			 // 测试函数：有效性验证
├── README.md					// Github readme 文档
├── requirements.txt				// 程序运行环境
└── main.py						// 程序入口
```

### 项目运行

#### 命令行方式

##### 1.生成题目功能

```
python main.py -n [生成的表达式数量] -r [数值上届]
```
要求 [生成的表达式数量] 为正整数，[数值上界] 为 大于1、小于10的正整数

##### 2.判题功能

```
python main.py -e [题目路径] -a [答案路径]
```
要求 [题目路径]、[答案路径] 均为对应 .txt 文件的绝对路径

#### 图形化界面

##### 1.程序入口

主目录下选择`main.py`，点击运行按钮开始程序的执行，进入主界面

![Snipaste_2024-09-25_14-28-39](https://github.com/user-attachments/assets/5f43222a-db65-4108-ae16-0d427fb9e90b)

##### 2.生成题目功能

1. 首先输入`题目数量`和`数值上届`
2. 然后点击`生成题目`按钮
3. 等待程序完成
4. 最后查看当前目录下的`Exercises.txt`和`Answers.txt`，即生成的文件

![2](https://github.com/user-attachments/assets/5026327b-b00d-40c4-b8fa-49b459effc45)

##### 3.判题功能

1. 首先点击`判题`按钮
2. 然后选择文件
3. 等待程序完成
4. 最后查看当前目录下的`Grade.txt`，即生成的文件

