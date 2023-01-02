from static import doc_settings
from sys import exit
from typecheck import checkType, Num

############################################
#        DPL Function Parent Classes

class Func:
    """Parent class of all functions used in DPL."""
    dpl_func = True               # all
    # inputs (options and content)
    options_optl = False          # some
    options_redq = False          # some
    content_reqd = False          # some
    # function placement/usage
    top_level = False             # some
    nest_level = False            # some
    inside_gates = False          # some
    outside_gates = False         # some
    # can be assigned to user-defined variable
    returns_obj = False           # some
    def __new__(cls):
        raise NotImplementedError(f"{cls} base class cannot be instantiated.")

class GlobalFunc(Func):
    """Parent class of all functions meant to adjust global settings of the document."""
    # inputs (options and content)
    options_optl = False          # all
    options_reqd = True           # most (exception: RunCodeFunc)
    content_reqd = False          # most (exception: RunCodeFunc)
    # function placement/usage
    top_level = True              # all
    nest_level = False            # all
    inside_gates = False          # all
    outside_gates = True          # all
    # can be assigned to user-defined variable
    returns_obj = False           # some

class SettingsFunc(GlobalFunc):
    """Parent class of all functions meant to adjust global settings of the document."""
    # can be assigned to user-defined variable
    returns_obj = False           # all

class ImportFunc(GlobalFunc):
    """Parent class of all functions meant to import functions or content."""
    # can be assigned to user-defined variable
    returns_obj = True            # all

class RunCodeFunc(GlobalFunc):
    """Parent class of runCode function."""
    # inputs (options and content)
    options_reqd = False          # all
    content_reqd = True           # all
    # can be assigned to user-defined variable
    returns_obj = True            # all

class ContentFunc(Func):
    """Parent class of all functions that are meant to produce content."""
    # inputs (options and content)
    options_optl = False          # some
    options_redq = False          # some
    content_reqd = False          # some
    # function placement/usage
    top_level = True              # some
    nest_level = True             # all
    inside_gates = True           # all
    outside_gates = True          # some
    # can be assigned to user-defined variable
    returns_obj = True            # all

class SymbolFunc(ContentFunc):
    """Parent class of all content functions that produce only static one-character symbols."""
    # inputs (options and content)
    options_optl = True           # some
    options_redq = False          # all
    content_reqd = False          # all
    # function placement/usage
    top_level = False             # all
    nest_level = True             # all
    inside_gates = True           # all
    outside_gates = False         # all


############################################
#              Document Class

class Document:
    settings = doc_settings
    namespace = {}
    doc_contents = {}


############################################
#              Error Class

class Error:
    error_type = "DocuposeError"
    def __init__(self, message, line_num, line):
        checkType(
            ("message", str, message),
            ("line_num", Num((0, None), num_type=int), line_num),
            ("line", str, line),
        )
        print(f"Line {line_num}:\n\t{line}\n{self.error_type}: {message}")
        exit()