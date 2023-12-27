# 开发文档
风格：
满分15分，其中代码注释6分，命名6分，其它3分。
设计和实现：
满分30分，其中数据结构7分，模块划分7分，功能8分，文档8分。
接口：
满分15分，其中程序间接口8分，人机接口7分。
测试：
满分30分，测试桩15分，自动测试脚本15分
记法：
满分10分，文档中对此脚本语言的语法的准确描述。



- 设计和实现：功能：多线程 文档：sphinx
- 程序间接口：python模块、数据库    人机接口：简单GUI/CLI、配置文件、日志
- 测试：单元测试库

记法

## 风格

代码格式化采用PEP8标准，其余风格见下

### 注释

采用reStructuredText风格，这也是sphinx默认的风格。

示例如下：

```python
@staticmethod
    def update(src_dict: dict, target_dict: dict):
        """
        update the src dict with target dict. Not like the builtin dict().update, this will update recursively.

        :param src_dict: src dict
        :param target_dict: target dict
        :return: updated dict
        """
        # ...
```

### 命名风格

命名应遵循以下风格：

- 类名使用大驼峰命名法，如： `CodeGenerator, Parser`等
- 类的公开成员方法使用下划线命名法，如： `pretty_print，parse `
- 类的私有方法使用双下划线+下划线命名法，如： `__assign, __calc_expr`
- 变量名使用下划线命名法，如：`user_input`
- 文件名，包名尽量使用下划线命名法，除非有约定俗成的大写字母缩写，如：`code_generator.py` , `DSL`

### 模块组织

- 尽量一个模块对应一个类，如`parser.py`对应`Parser`类，除非该模块没有类或者必要的有很多类，如`object_code.py`包含了生成的目标代码所应该具有的各种数据结构类。
- 在每个包的`__init__.py`中`import`需要暴露给外部的接口，也可显式地定义`__all__ = []`来确定接口

### commit风格

采用前端框架[Angular提出的git commit规范](https://zj-git-guide.readthedocs.io/zh-cn/latest/message/Angular%E6%8F%90%E4%BA%A4%E4%BF%A1%E6%81%AF%E8%A7%84%E8%8C%83/)，如下

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

提交类型指定为下面其中一个：

1. `build`：对构建系统或者外部依赖项进行了修改
2. `ci`：对CI配置文件或脚本进行了修改
3. `docs`：对文档进行了修改
4. `feat`：增加新的特征
5. `fix`：修复`bug`
6. `pref`：提高性能的代码更改
7. `refactor`：既不是修复`bug`也不是添加特征的代码重构
8. `style`：不影响代码含义的修改，比如空格、格式化、缺失的分号等
9. `test`：增加确实的测试或者矫正已存在的测试

## 设计和实现

设计上，程序类似c语言的编译流程。Parser将源代码（`.ys`，yard service）文件进行词法、语法分析后生成抽象语法树AST，CodeGenerator将语法树转化为目标代码(`.yo`，yard object code)，Interpreter解释执行目标代码。

### 数据结构

#### 抽象语法树AST

采用lark库的语法树，由Tree类和Token类嵌套组成。类似：

```python
Tree('service', [
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['MyStep'])]),
                    Tree('step_body', [
                        Tree('command',
                             [Tree('assign',
                                   [Tree('var', ['$var']), Tree('expression', [Tree('term', ['"value"'])])])]),
                        Tree('command', [Tree('speak', [Tree('expression', [Tree('term', ['"Hello, World!"'])])])]),
                    ])
                ]),
            ])
```

将其以更可读的形式打印出来如下：

```
service
  step_block
    step_header
      step_name	MyStep
    step_body
      command
        assign
          var	$var
          expression
            term	"value"
      command
        speak
          expression
            term	"Hello, World!"
```

#### 目标代码

目标代码是一个Service类，将其序列化为文件即为目标代码文件。详细定义在object_code.py中。可以将其看成是C++的嵌套结构体。比如Service就是一系列Step的元组，而Step又是由步骤名和一系列指令Command组成的元组，每条指令类似三地址代码，是参数的元组，以此类推。

```python
class Service:
    def __init__(self, steps: tuple[Step]):
        self.steps: tuple[Step] = steps
	def __str__(self):
    	return str(self.steps)

	def __repr__(self):
    	return self.__str__()
```

把一个实际的Service类以嵌套元组的形式打印出来结果如下：

```python
(('MyStep', (('assign', ('$$var', ('"value"',))), ('speak', (('"Hello, World!"',),)))),),
```

#### 变量表

由interpreter维护一个哈希表作为变量表

```python
self.__variables: dict[str:str] = {
    "$foo" : "123",
    "$bar" : "456"
}
```

### 模块划分

### 功能

### 文档

## 接口

### 程序间接口

### 人机接口

## 测试

### 测试桩

### 自动测试脚本

## 记法

### DSL语法记法

### 配置文件记法