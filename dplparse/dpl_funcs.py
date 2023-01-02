from classes import Document
from classes import SettingsFunc, RunCodeFunc, ImportFunc, ContentFunc, SymbolFunc



###########################################
#          Settings Functions

class setContentStyle(SettingsFunc):
    """Set the font style for text, math or code content"""
    def __new__(cls, doc: Document, 
                renderType, font="default", size=12, emph="ef", color="#000000", 
                bgColor=None, borderWidth=0, borderColor=None, borderRadius=0):
        key = doc.settings[renderType]
        key["font"] = font
        key["size"] = size
        if emph != "ef":
            key["emph"] = emph
        key["color"] = color
        if bgColor:
            key["bg-color"] = bgColor
        if borderWidth:
            key["border-width"] = borderWidth
            if borderColor:
                key["border-color"] = borderColor
        if (bgColor or borderWidth) and borderRadius:
            key["border-radius"] = borderRadius

class setPageNumbers(SettingsFunc):
    """Set page numbers (PDF only)"""
    def __new__(cls, doc: Document, 
                num_type="numbers", start_num=0, start_pg=1, evens_only=False):
        pass # TODO: pdf

class setOutput(SettingsFunc):
    """Set the type and destination of Docupose rendering. Use extensions .pdf or .html for `name`."""
    def __new__(cls, doc: Document, 
                name="main", size="default"):
        pass # TODO

class setArgs(SettingsFunc):
    """Set default arguments for the options of content functions."""
    def __new__(cls, doc: Document, func, **kwargs):
        pass



###########################################
#            Import Functions

class importPackage(ImportFunc):
    """Import a package into the namespace. Functions can be accessed with the @ operator."""
    def __new__(cls, doc: Document, 
                pkgLocation):
        pkgLocation
        doc.namespace[pkgLocation]

class importFrom(ImportFunc):
    """Import a specific function from a package."""
    def __new__(cls, doc: Document, objName, pkgName):
        pass

class importContent(ImportFunc):
    """Import text, math or code content from another file."""
    def __new__(cls, doc: Document, fileName, renderType="text"):
        pass



###########################################
#            RunCode Function

class runCode(RunCodeFunc):
    """Run python code that can access and adjust the namespace of the document."""
    def __new__(cls, doc: Document, content):
        pass



###########################################
#       Content-Producing Functions

class bf(ContentFunc):
    receives_options = True
    receives_content = True
    allowed_use = (TOP_LEVEL, NESTED, INSIDE_RGS, OUTSIDE_RGS)
    def __new__(cls, doc: Document, content):
        pass

class it(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class un(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class ef(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class text(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class math(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class code(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class title(ContentFunc):
    def __new__(cls, doc: Document, *content):
        pass

class section(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class subsection(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class contents(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class columns(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class columnbreak(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class image(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class list(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class framed(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class caption(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class footnote(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class citations(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class quote(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class color(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class strike(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class smallcaps(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class align(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass

class centerAligned(ContentFunc):
    def __new__(cls, doc: Document, content):
        pass


###########################################
#       Symbol Functions

class newline(SymbolFunc):
    """Add newline(s). 
    For convenience, it is recommended to use shorthand instead: \\\\"""
    receives_options = True
    def __new__(cls, doc: Document, num=1):
        pass

class t(SymbolFunc):
    """Add indent(s) or tab(s)."""
    receives_options = True
    def __new__(cls, doc: Document, num=1):
        pass

class s(SymbolFunc):
    """Add space(s)."""
    receives_options = True
    def __new__(cls, doc: Document, num=1):
        pass

class quotationmark(SymbolFunc):
    """Add quotation mark (i.e., \"), with optional symbol type open (i.e., O) or close (i.e., C). 
    For convenience, it is recommended to use one of these shorthands instead: \\\" for \\quotationmark, \\qo for \\quotationmark[O], or \\qc for \\quotationmark[C]"""
    receives_options = True
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class qo(SymbolFunc):
    """Add opening quotation mark. Used as shorthand for \\q[O]"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class qc(SymbolFunc):
    """Add closing quotation mark. Used as shorthand for \\q[C]"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class dollar(SymbolFunc):
    """Add dollar sign (i.e., $). 
    For convenience, it is recommended to use shorthand instead: \\$"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class backtick(SymbolFunc):
    """Add backtick (i.e., `). 
    For convenience, it is recommended to use shorthand instead: \\`"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class pipe(SymbolFunc):
    """Add pipe (i.e., |). 
    For convenience, it is recommended to use shorthand instead: \\|"""
    receives_options = False
    def __new__(cls, doc: Document):
        pass

class bracket(SymbolFunc):
    """Add bracket (i.e., [ or ]) with symbol type open (i.e., O) or closed (i.e., C). 
    For convenience, it is recommended to use shorthand instead: \\[ for \\bracket[O], or \\] for \\bracket[C]"""
    receives_options = True
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class brace(SymbolFunc):
    """Add brace (i.e., { or }) with symbol type open (i.e., O) or closed (i.e., C). 
    For convenience, it is recommended to use shorthand instead: \\{ for \\brace[O], or \\} for \\brace[C]"""
    receives_options = True
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class at(SymbolFunc):
    """Add at-symbol (i.e., @).
    For convenience, it is recommended to use shorthand instead: \\@"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class pound(SymbolFunc):
    """Add pound (i.e., #).
    For convenience, it is recommended to use shorthand instead: \\#"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass