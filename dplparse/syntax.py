import re



#########################################
#                typed

# syntax symbols
syntax_syms = {
    "escape": "\\",              # symbol for function escape
    "text_gate": "\"",           # gate for text rendering
    "math_gate": "$",            # gate for math rendering
    "code_gate": "`",            # gate for code rendering
    "l_bracket": "[",            # left lid for options and arrays
    "r_bracket": "]",            # right lid for options and arrays
    "l_brace": "{",              # left lid for content and groups
    "r_brace": "}",              # right lid for content and groups
    "ministr_gate": "'",         # ministr gate
    "color_prefix": "#",         # prefix for dptype color
    "comment_sym": "%",          # symbol to start end-of-line comments
    "sep_sym": "|",              # separator symbol
    "at_sym": "@",               # symbol to set alignment or access functions from modules
    "2d_sep_sym": "&",           # symbol to separate lists in stream shorthand
    "superscript_sym": "^",      # symbol to set superscript
    "subscript_sym": "_",        # symbol to set subscript
    "add_sym": "+",              # symbol for addition
    "minus_sym": "-",            # symbol for subtraction
    "param_set_sym": "=",        # symbol for setting parameters
    "assignment_op_sym": "<-",   # symbol to assign content to variable
}



#########################################
#                rendered

def _getGateRegex(gate, num):
    gate = re.escape(gate)
    return f"(?<!{gate})" + gate*num + f"(?!{gate})" + "|" + \
        f"(?<={re.escape(escape)}{gate})" + gate*num + f"(?!{gate})"

# plain strings
escape = syntax_syms["escape"]
newline = escape * 2
gate_types = tuple(syntax_syms[f"{i}_gate"] for i in ("text", "math", "code"))
all_gates = tuple(gate*num for gate in gate_types for num in range(1,4))
option_lids = array_lids = tuple(syntax_syms[f"{i}_bracket"] for i in ("l", "r"))
content_lids = group_lids = tuple(syntax_syms[f"{i}_brace"] for i in ("l", "r"))
open_lids, close_lids = (tuple(syntax_syms[f"{i}_brac{j}"] for j in ("e", "ket")) for i in ("l", "r"))
ministr_gate = syntax_syms["ministr_gate"]
color_prefix = syntax_syms["color_prefix"]
comment_sym = syntax_syms["comment_sym"]                        
sep_sym = syntax_syms["sep_sym"]
align_sym = access_sym = syntax_syms["at_sym"]
sep2_sym = syntax_syms["2d_sep_sym"]
sup_sym = syntax_syms["superscript_sym"]
sub_sym = syntax_syms["subscript_sym"]
add_sym = syntax_syms["add_sym"]
minus_sym = syntax_syms["minus_sym"]
param_set_sym = syntax_syms["param_set_sym"]
assign_sym = syntax_syms["assignment_op_sym"]
# regex patterns
no_escape_regex = f"(?<!{re.escape(escape)})"                                        # matches anything not escaped
escape_regex = f"{re.escape(escape)}{re.escape(escape)}?"                            # matches proper function escape slashes
variable_names_regex = f"{re.escape(escape)}[A-Za-z][A-Za-z0-9]*(?![A-Za-z0-9])"     # matches any valid function name
func_shorthand_regex = f"{re.escape(escape)}\\S"
ministr_gate_regex = no_escape_regex + ministr_gate
render_gate_regex = "|".join(_getGateRegex(gate, num) for gate in gate_types for num in range(1,4))
open_lid_regex = "|".join(map(re.escape, open_lids))
close_lid_regex = "|".join(map(re.escape, close_lids))
open_enclosers_regex = "|".join((ministr_gate_regex, render_gate_regex, open_lid_regex))
enclosers_regex = "|".join((open_enclosers_regex, close_lid_regex))
next_func_regex = "|".join((render_gate_regex, variable_names_regex, func_shorthand_regex))