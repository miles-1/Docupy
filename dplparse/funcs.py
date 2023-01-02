from os.path import basename
from static import symbol_shorthands
import re

re.count = lambda pattern, string: len(re.findall(pattern, string))

def parsedpl(file_contents):
    render_brackets = ("\"", "$", "`")
    all_render_brackets = tuple(f"(?<!{bracket})" + bracket*num + f"(?!{bracket})" \
                                for bracket in render_brackets for num in range(1,4))
    lines = tuple(file_contents.split("\n"))
    num_lines = len(lines)
    current_num = 0
    last_bracket = None
    while current_num < num_lines:
        current_line = lines[current_num].strip()
        if current_line[0] == "\\":
            pass




    # Replace symbol shorthands
    for shorthand in symbol_shorthands.items():
        file_contents = file_contents.replace(*shorthand)
    # Replace render brackets with corresponding tags
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
