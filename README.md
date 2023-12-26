# YARD
Yet another robot DSL for customer service.

## EBNF语法

[EBNF](https://www.wikiwand.com/en/Extended_Backus%E2%80%93Naur_form)是一种扩展的BNF语法，本项目的EBNF语法如下。

```
service     : step_block*
step_block  : step_header step_body
step_header : "step" step_name
step_name   : CNAME
step_body   : command*
command     : assign | speak | listen | branch | silence | default | exit | runpy | system
assign      : var "=" expression
expression  : term ("+" term)*
term        : var | ESCAPED_STRING
var         : "$" CNAME
speak       : "speak" expression
listen      : "listen" expression ["," var]
branch      : "branch" expression "," step_name
silence     : "silence" step_name
default     : "default" step_name
exit        : "exit"
runpy       : "runpy" expression
system      : "system" expression                
```

其中，`CNAME`是预定义的变量名语法，和C/C++的变量名语法相同，其值为`("_"|LETTER) ("_"|LETTER|DIGIT)*`，`LETTER`和`DIGIT`也是预定义的字母和数字。`ESCAPED_STRING`是带转义规则的字符串，需要用`""`包括。

同时，也会正确忽略空白字符以及支持C/C++注释风格。

## 语法解释

一个客服机器人服务`service`由多个分支步骤`step`组成，`step`后接此分支的名字。

每个分支可以定义多条指令，它们是`assign | speak | listen | branch | silence | default | exit | runpy | system`

- `assign`：赋值语句，给变量赋值
- `speak`：给客户发送信息
- `listen`：等候一定的秒数，将客户的回复储存于内部变量`$_last_response`，同时可选将回复也复制到指定的变量中
- `branch`：将`$_last_response`的值与给定值匹配，如果相等则进入指定的分支
- `silence`：如果客户没有回复，也即`$_last_response`的值为空串，则进入指定的分支
- `default`：如果以上都不匹配，默认进入指定的分支
- `exit`：退出会话
- `runpy`：执行python语句
- `system`：执行系统命令

变量以`$`开头，之后命名规则与C/C++相同，所有数据/变量都是字符串，加法运算就是字符串拼接。
