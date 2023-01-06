import re
from funcs import typeIfNum


############################################
#            Parent dptype Class

class dptype:
    """
    Types used in docupose, with a few exceptions:
        - DP uses python's bool, int, and float. 
        - DP uses python's Nonetype, but renames it nonetype.
        - DP uses ministr as wrapper for python's str.
        - DP uses array as wrapper for python's list, but it has fixed size unlike list.
    """
    pass



############################################
#      keyword_dptype Class & Children

class keyword_dptype(dptype):
    possible_vals = []
    def __init__(self, obj):
        self.val = obj
    def __str__(self):
        return str(self.val)
    def __eq__(self, string):
        return self.val == string
    def get(self):
        return self.val

class display(keyword_dptype):
    possible_vals = ["Inline", "Block", "InlineBlock", "Full"]
    @staticmethod
    def isinstance(string):
        return string in display.possible_vals

class position(keyword_dptype):
    possible_vals = ["L", "U", "R", "D", "M", "UL", "UR", "DL", "DR", "LR", "UD"]
    @staticmethod
    def isinstance(string):
        return string in position.possible_vals

class emphtype(keyword_dptype):
    possible_vals = ["EF", "BO", "IT", "UN", "SMC", "SUP", "SUB"]
    def __init__(self, obj):
        """When this class is used externally, obj should always be a single value from self.possible_values."""
        if isinstance(obj, str):
            super().__init__([obj])
        elif isinstance(obj, list):
            if all(i in self.possible_vals for i in obj):
                super().__init__(list(set(obj)))
            elif all(isinstance(i, emphtype) for i in obj):
                val_set, su_script = set(), None
                su_options = {"SUB", "SUP"}
                for e in obj:
                    intersect = su_options.intersection(set(e.val))
                    if intersect:
                        su_script = intersect.pop()
                    val_set.update(e.val)
                if "EF" in val_set:
                    val_set = {"EF"}
                elif su_script in su_options and (su_options - {su_script}).pop() in val_set:
                    val_set -= su_options - {su_script}
                super().__init__(list(val_set))
    @staticmethod
    def isinstance(string):
        return string in emphtype.possible_vals
    def __add__(self, obj):
        if isinstance(obj, emphtype):
            val1, val2 = self.val, obj.val
            if ["EF"] == val2:
                return emphtype("EF")
            elif ["EF"] == val1:
                return emphtype([obj])
            else:
                return emphtype([self, obj])
        else:
            raise TypeError(f"Cannot add types emphtype and {type(obj)}.")
    def __sub__(self, obj):
        if isinstance(obj, emphtype):
            diff = set(self.val) - set(obj.val)
            return emphtype(list(diff)) if diff else emphtype("EF")
        else:
            raise TypeError(f"Cannot add types emphtype and {type(obj)}.")



############################################
#     content_dptype Class & Children

class content_dptype(dptype):
    pass

class group(content_dptype):
    pass

class necklace(content_dptype):
    pass

class image(content_dptype):
    def __init__(self, path, **style):
        self.path = path
        self.style = style

class textlike_dptype(content_dptype):
    def __init__(self, string, **style):
        self.content = string
        self.style = style
    def __str__(self):
        return self.content

class text(textlike_dptype):
    pass

class math(textlike_dptype):
    pass

class code(textlike_dptype):
    pass



############################################
#     pattern_dptype Class & Children

class pattern_dptype(dptype):
    pass

class color(pattern_dptype):
    prefix = "#"
    possible_lengths = {6: "[A-Fa-f0-9]{6}", 8: "[A-Fa-f0-9]{8}"}
    def __init__(self, string):
        string = string.lower()
        string = string[1:]
        self.val = string[:6] + (string[6:] if len(string) == 8 else "ff")
    def getRGBA(self):
        return tuple(int(self.hex[i:i+2], 16) for i in range(0,6,2)) + (int(self.alpha, 16),)
    @staticmethod
    def isinstance(string):
        if not string \
           or not isinstance(string, str) \
           or string[0] != color.prefix:
            return False
        string = string[1:]
        string_length = len(string)
        if string_length not in color.possible_lengths:
            return False
        pattern = color.possible_lengths[string_length]
        return re.match(pattern, string) != None

class ministr(str, pattern_dptype):
    gate = "'"
    def __init__(self, string):
        self.val = string
    @staticmethod
    def isinstance(string):
        if not all(string[i] == ministr.gate for i in (-1, 0)):
            return False
        string = string[1:-1]
        return re.search(ministr.regex, str) == None

class array(list, pattern_dptype):
    left_gate = "["
    right_gate = "]"
    sep = "|"
    def __init__(self, string):
        self.val = string[1:-1].split(array.sep)
    def __add__(self, array_2):
        if isinstance(array_2, array):
            return
    @staticmethod
    def isinstance(string):
        if not string[0] == array.left_gate or not string[-1] == array.right_gate:
            return False
        string = string[1:-1].split(array.sep)



############################################
#   dptype namespace & string conversion

dptype_literals = {
    "None": None,
    "True": True,
    "False": False,
}
dptype_namespace = {
    "bool": bool,
    "int": int,
    "float": float,
    "nonetype": type(None),
}
local_namespace = locals().copy()
for string, obj in local_namespace.items():
    if isinstance(obj, type) and issubclass(obj, dptype) \
    and hasattr(obj, "__name__") and "dptype" not in obj.__name__:
        dptype_namespace[string] = obj
        if hasattr(obj, "possible_vals"):
            for val in obj.possible_vals:
                dptype_literals[val] = obj(val)

def getDPtype(string):
    string = string.strip()
    if string in dptype_namespace and \
        isinstance(dptype_namespace[string], type) or \
        string in ("int", "float", "bool", "nonetype"):
        return dptype
    for dpt in dptype_namespace.values(): 
        if hasattr(dpt, "isinstance") and dpt.isinstance(string):
            return dpt
    if string == "None":
        return type(None)
    if string in ("True", "False"):
        return bool
    return typeIfNum(string)
    
class dptypedict(dict):
    def __init__(self, obj):
        self.stringdict = dict(obj)
        super().__init__(obj)
    def __getitem__(self, string):
        if isinstance(string, str):
            if string in self.stringdict:
                return self.stringdict[string]
            if j := typeIfNum(string):
                if j == int:
                    return int(string)
                elif j == float:
                    return float(string)
            raise TypeError(f"Cannot interpret string {string}")
        else:
            raise TypeError("Cannot accept nonstring.")

dptype_literals = dptypedict(dptype_literals)