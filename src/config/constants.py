"""
This module contains program constants. Including EBNF, config_path, etc.
"""

EBNF = """
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

%import common (ESCAPED_STRING, WS, CNAME, C_COMMENT, CPP_COMMENT)
%ignore WS
%ignore C_COMMENT
%ignore CPP_COMMENT
"""

"""
EBNF grammar constants
"""

log_format = "[%(asctime)s %(name)s %(levelname)s] %(message)s"
"""
logging format
"""

config_path = "config.yaml"
default_config_path = "src/config/default.yaml"
