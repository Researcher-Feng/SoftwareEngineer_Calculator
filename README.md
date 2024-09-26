## 软件工程-四则运算生成器



### 运行环境

以下是基本需求（更详细的环境需求请参考`requirements.txt`）：

- Python 3.9.13
- line-profiler-pycharm==1.1.0
- line_profiler==4.1.3

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
│   ├── test_eval.py	  // 测试函数：字符串数学化
│   ├── test_evaluate.py	  // 测试函数：字符串预处理
│   ├── test_generate.py		  // 测试函数：表达式生成
│   └── test_valid.py			 // 测试函数：有效性验证
├── README.md					// Github readme 文档
├── requirements.txt				// 程序运行环境
└── main.py						// 程序入口
```

### 项目运行

#### 1.程序入口

主目录下选择`main.py`，点击运行按钮开始程序的执行，进入主界面

![Snipaste_2024-09-25_14-28-39](D:\我的文档\Desktop\学校\软件工程\作业\3结对项目\UI界面\Snipaste_2024-09-25_14-28-39.jpg)

#### 2.生成题目功能

1. 首先输入`题目数量`和`数值上届`
2. 然后点击`生成题目`按钮
3. 等待程序完成
4. 最后查看当前目录下的`Exercises.txt`和`Answers.txt`，即生成的文件

![2](D:\我的文档\Desktop\学校\软件工程\作业\3结对项目\UI界面\2.jpg)

![Snipaste_2024-09-25_14-51-11](D:\我的文档\Desktop\学校\软件工程\作业\3结对项目\UI界面\Snipaste_2024-09-25_14-51-11.jpg)

#### 3.判题功能

1. 首先点击`判题`按钮
2. 然后选择文件
3. 等待程序完成
4. 最后查看当前目录下的`Grade.txt`，即生成的文件

![Snipaste_2024-09-25_14-29-28](D:\我的文档\Desktop\学校\软件工程\作业\3结对项目\UI界面\Snipaste_2024-09-25_14-29-28.jpg)

![Snipaste_2024-09-25_14-30-08](D:\我的文档\Desktop\学校\软件工程\作业\3结对项目\UI界面\Snipaste_2024-09-25_14-30-08.jpg)