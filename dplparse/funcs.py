from syntax import gate_types, open_lids, close_lids, ministr_gate, escape, escape_regex
from dptypes import getDPType, getDPLiteral, getDPFunc
from classes import parse_str, nomatch
from classes import DP_SyntaxError
import re





def dpeval(string, namespace):
    if isinstance(string, str):
        lines = string.split("\n", string_only=True)
        obj = parse_str(string)
        result = _dpeval_recursive(obj, namespace)
        if isinstance(result, tuple):
            error_type, line_num, message = result
            raise error_type(message, line_num, lines[line_num])
        elif isinstance(result, list):
            return result # TODO idek lol
    else:
        raise TypeError("Cannot evaluate nonstring.")

def _dpeval_recursive(obj, namespace):
    if isinstance(obj, parse_str):
        commands = []
        for line in obj.split(escape_regex):
            if line[0] == escape:
                pass


def countSymbols(string, regex, pre_indx, post_indx):
    return re.count(regex, string[:pre_indx]) % 2 and re.count(regex, string[post_indx:]) % 2

def getSepdEntries(string, convert_literals=True):
    pipes = tuple(i.start() for i in re.finditer("(?<!\\\\)\|", string))
    top_level_pipes = []
    for indx in pipes:

        outside_render_gates = not any(countSymbols(string, gate_regex, indx, indx+1) for gate_regex in all_render_gates)
        outside_other_gates = all(string[:indx].count(e[0]) == string[:indx].count(e[1]) for e in lid_enclosers)
        not_in_ministr = not re.count("(?<!\\\\)'", string[:indx]) % 2
        if outside_render_gates and outside_other_gates and not_in_ministr:
                top_level_pipes.append(indx)
    start_indices = [None] + list(i+1 for i in top_level_pipes)
    end_indices = top_level_pipes + [None]
    entries = tuple(string[i:j].strip() for i, j in zip(start_indices, end_indices))
    return entries

def getOptionArgs(string, line, line_num):
    args = getSepdEntries(string)
    option_dict = {}
    keyword_arg_started = False
    for num, arg in enumerate(args):
        if re.match("[A-Za-z][A-Za-z0-9]+\\s+=", arg):
            param_name, value = (i.strip() for i in arg.split("=", 1))
            option_dict[param_name] = value
            keyword_arg_started = True
        elif re.match("'.+'", arg, re.DOTALL):
            option_dict[num] = re.sub("\\s+", " ", arg)
        elif re.match("[^'].+=", arg, re.DOTALL):
            DP_SyntaxError("Invalid syntax for parmater name", line_num, line)
        elif not keyword_arg_started:
            option_dict[num] = value
        else:
            DP_SyntaxError("positional argument follows keyword argument", line_num, line)
    return option_dict
