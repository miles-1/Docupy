from os.path import basename
from static import symbol_shorthands
import re
from classes import DP_SyntaxError

re.count = lambda pattern, string: len(re.findall(pattern, string))

def parsedpl(file_contents):
    render_gates = ("\"", "$", "`")
    all_render_gates = tuple(f"(?<!{gate})" + gate*num + f"(?!{gate})" \
                                for gate in render_gates for num in range(1,4))
    lines = tuple(file_contents.split("\n"))
    num_lines = len(lines)
    current_num = 0
    gates = []
    while current_num < num_lines:
        current_line = lines[current_num].strip()
        if current_line[0] == "\\":
            pass




    # Replace symbol shorthands
    for shorthand in symbol_shorthands.items():
        file_contents = file_contents.replace(*shorthand)
    # Replace render gates with corresponding tags
    display_types = {
        1: "inline",
        2: "block",
        3: "full"
    }
    


def checkFunction(string, namespace):
    if not re.match("\\\\[A-Za-z][A-Za-z0-9]+", string):
        pass


def getPkgName(pkgPath):
    basename = basename(pkgPath)
    re.split("[\-\_]", basename)

def getGateRegex(gate, num):
    escape = "\\" if gate == "$" else ""
    return f"(?<!{escape}{gate})" + gate*num + f"(?!{gate})" + "|" + \
        f"(?<=\\\\{escape}{gate})" + gate*num + f"(?!{gate})"

def getArrayEntries(string):
    pipes = tuple(i.start() for i in re.finditer("(?<!\\\\)\|", string))
    top_level_pipes = []
    for indx in pipes:
        render_gates = ("\"", "$", "`")
        all_render_gates = tuple(getGateRegex(gate, num) for gate in render_gates for num in range(1,4))
        other_gates = (("[", "]"), ("{", "}"))
        outside_render_gates = not any(re.count(gate_regex, string[:indx]) % 2 for gate_regex in all_render_gates)
        outside_other_gates = all(string[:indx].count(brac[0]) == string[:indx].count(brac[1]) for brac in other_gates)
        not_in_ministr = not re.count("(?<!\\\\)'", string[:indx]) % 2
        if outside_render_gates and outside_other_gates and not_in_ministr:
                top_level_pipes.append(indx)
    start_indices = [None] + list(i+1 for i in top_level_pipes)
    end_indices = top_level_pipes + [None]
    entries = tuple(string[i:j].strip() for i, j in zip(start_indices, end_indices))
    return entries

def getOptionArgs(string, line, line_num):
    args = getArrayEntries(string)
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

def parseOptionValue(value):
    pass

def typeIfNum(string):
    string = re.sub("^-", "", string)
    if re.match("^[0-9]+$", string):
        return int
    string = re.sub(".", "", string, 1)
    if re.match("^[0-9]+$", string):
        return float