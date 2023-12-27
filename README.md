# YARD
YARD 是"Yet another robot DSL for customer service" 的缩写。

北京邮电大学2021级 程序设计实践 大作业

## 介绍

本项目实现了一个领域特定语言(DSL)用于编写客服机器人应答逻辑。使得能够通过简单的编写脚本就能改变客服逻辑而不用更改源代码，适用于需求经常变化的场景。此语言相对简单，编写门槛较低。

文法中内置了几种常用命令，例如向用户发送信息，等待用户回复等。文法也支持用户直接运行Python代码、执行系统shell指令来扩展功能或与外界模块交互。

## EBNF语法

[EBNF](https://www.wikiwand.com/en/Extended_Backus%E2%80%93Naur_form)是一种扩展的BNF语法，本项目的EBNF语法如下。

```
service     : step_block*
step_block  : step_header step_body
step_header : "step" step_name
step_name   : CNAME
step_body   : command*
command     : assign | speak | listen | branch | silence | default | end | runpy | system
assign      : var "=" expression
expression  : term ("+" term)*
term        : var | ESCAPED_STRING
var         : "$" CNAME
speak       : "speak" expression
listen      : "listen" expression ["," var]
branch      : "branch" expression "," step_name
silence     : "silence" step_name
default     : "default" step_name
end         : "end"
runpy       : "runpy" expression
system      : "system" expression    
```

其中，`CNAME`是预定义的变量名语法，和C/C++的变量名语法相同，其值为`("_"|LETTER) ("_"|LETTER|DIGIT)*`，`LETTER`和`DIGIT`也是预定义的字母和数字。`ESCAPED_STRING`是带转义规则的字符串，需要用`""`包括。

同时，也会正确忽略空白字符以及支持C/C++注释风格。

### 语法解释

一个客服机器人服务`service`由多个分支步骤`step`组成，`step`后接此分支的名字。

每个分支可以定义多条指令，它们是`assign | speak | listen | branch | silence | default | exit | runpy | system`

变量以`$`开头，之后命名规则与C/C++相同，所有变量/表达式的最终值都是字符串，加法运算就是字符串拼接。

- `assign` ：赋值语句，给变量赋值 e.g. `$foo = "1"`
- `speak <expression>`：给客户发送信息 
- `listen <time_expression> [, $var] `：等候一定的秒数，将客户的回复储存于内部变量`$_last_response`，同时可选将回复也复制到指定的变量`$var`中
- `branch <to_match_expression> <next_step>`：将`$_last_response`的值与给定值匹配，如果相等则进入指定的分支
- `silence <next_step>`：如果客户没有回复，也即`$_last_response`的值为空串，则进入指定的分支
- `default <next_step>`：如果以上都不匹配，默认进入指定的分支
- `end`：结束会话
- `runpy <code_expression>`：执行python语句
- `system <command_expression>`：执行系统命令

### 示例脚本

见[services](https://github.com/Emofer/YARD/tree/main/services)目录下的.ys文件。`.ys`意思是`yard service`

## 安装

需要python3.8+版本，在项目根目录下运行

```sh
pip install -r requirements.txt
```

来安装依赖。

## 使用说明

### 配置文件

程序会读取工作目录下的`config.yaml`，完整的配置文件如下，可以省略部分配置，会采取默认值。默认值位于`src/config/default.yaml`。

```yaml
# working dir of main interpreter.
pwd: .

# log config
log:
  level: INFO # log level, could be DEBUG, INFO, WARNING, ERROR, CRITICAL
  path: YARD.log # log path, could be relative or absolute path

# service config
service:
  path: ./services/customer.ys # path of service file, "ys" means "YARD service"
  variables: { } # variables passed to interpreter

```

### 运行

编写好自己的脚本文件`.ys`，在配置文件里设置为该文件路径，然后在根目录执行main.py

```sh
python main.py
```

### 文档构建

在`docs/`目录执行

```sh
make html
```

将会生成build目录，里面包含构建的文档。

开发文档/报告/模块API 见sphinx生成的网页文档，位于`docs/build/html/index.html`
