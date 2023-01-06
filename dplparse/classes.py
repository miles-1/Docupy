from static import doc_settings
from sys import exit
from typecheck import checkType, Num



############################################
#        DPL Function Parent Class

class Func:
    """Parent class of all functions used in DPL."""
    dpfunc = True                 # all
    # inputs (options and content)
    options_optl = False          # some
    options_redq = False          # some
    content_acpd = False          # some
    # function placement/usage
    top_level = False             # some
    nest_level = False            # some
    inside_gates = False          # some
    outside_gates = False         # some
    # can be assigned to user-defined variable
    returns_obj = False           # some
    def __new__(cls):
        raise NotImplementedError(f"{cls} base class cannot be instantiated.")



############################################
#  Global Function Parent Class & Children

class GlobalFunc(Func):
    """Parent class of all functions meant to adjust global settings of the document."""
    # inputs (options and content)
    options_optl = False          # all
    options_reqd = True           # most (exception: RunCodeFunc)
    content_acpd = False          # most (exception: RunCodeFunc)
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
    content_acpd = True           # all
    # can be assigned to user-defined variable
    returns_obj = True            # all



############################################
#  Content Function Parent Class & Children

class ContentFunc(Func):
    """Parent class of all functions that are meant to produce content."""
    # inputs (options and content)
    options_optl = False          # some
    options_redq = False          # some
    content_acpd = False          # some
    # function placement/usage
    top_level = False             # some
    nest_level = True             # all
    inside_gates = True           # all
    outside_gates = False         # some
    # can be assigned to user-defined variable
    returns_obj = True            # all

class SymbolFunc(ContentFunc):
    """Parent class of all content functions that produce only static one-character symbols."""
    # inputs (options and content)
    options_optl = True           # some
    options_redq = False          # all
    content_acpd = False          # all
    # function placement/usage
    top_level = False             # all
    outside_gates = False         # all

class FigFunc(ContentFunc):
    """Parent class of figure function"""
    # inputs (options and content)
    options_optl = False          # all
    options_redq = True           # all
    content_acpd = False          # all
    # function placement/usage
    top_level = True              # all
    outside_gates = True          # all

class StyleFunc(ContentFunc):
    """Parent class of all functions that style content."""
    # inputs (options and content)
    options_optl = False          # some
    options_redq = False          # some
    content_acpd = True           # all
    # function placement/usage
    top_level = True              # all
    outside_gates = True          # all
    # can be assigned to user-defined variable
    returns_obj = True            # all

class RefFunc(StyleFunc):
    """Parent class of all style functions that create references that can be used in some way elsewhere."""
    # inputs (options and content)
    options_optl = True           # all
    options_redq = False          # some

class RenderFunc(StyleFunc):
    """Parent class of all functions that produce rendertype content (text, math, code)"""
    # inputs (options and content)
    options_optl = True           # all
    options_redq = False          # all



############################################
#              Document Class

class Document:
    settings = doc_settings
    namespace = {}
    doc_contents = {}



############################################
#              Error Class

class DocuposeError:
    def __new__(cls, message, line_num, line):
        checkType(
            ("message", str, message),
            ("line_num", Num((0, None), num_type=int), line_num),
            ("line", str, line),
        )
        print(f"Line {line_num}:\n\t{line}\n{type(cls).__name__}: {message}")
        exit()

class DP_SyntaxError(DocuposeError):
    pass

class DP_ValueError(DocuposeError):
    pass

class DP_TypeError(DocuposeError):
    pass

