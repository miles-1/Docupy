from parser import Document

DEFAULT = ""



############################################
#        DPL Function Parent Class

class dpfunc:
    """Parent class of all functions used in DPL."""
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

class globalfunc(dpfunc):
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

class settingsfunc(globalfunc):
    """Parent class of all functions meant to adjust global settings of the document."""
    # can be assigned to user-defined variable
    returns_obj = False           # all

class importfunc(globalfunc):
    """Parent class of all functions meant to import functions or content."""
    # can be assigned to user-defined variable
    returns_obj = True            # all

class execfunc(globalfunc):
    """Parent class of runCode function."""
    # inputs (options and content)
    options_reqd = False          # all
    content_acpd = True           # all
    # can be assigned to user-defined variable
    returns_obj = True            # all



############################################
#  Content Function Parent Class & Children

class contentfunc(dpfunc):
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

class symbolfunc(contentfunc):
    """Parent class of all content functions that produce only static one-character symbols."""
    # inputs (options and content)
    options_optl = True           # some
    options_redq = False          # all
    content_acpd = False          # all
    # function placement/usage
    top_level = False             # all
    outside_gates = False         # all

class figfunc(contentfunc):
    """Parent class of figure function"""
    # inputs (options and content)
    options_optl = False          # all
    options_redq = True           # all
    content_acpd = False          # all
    # function placement/usage
    top_level = True              # all
    outside_gates = True          # all

class stylefunc(contentfunc):
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

class reffunc(stylefunc):
    """Parent class of all style functions that create references that can be used in some way elsewhere."""
    # inputs (options and content)
    options_optl = True           # all
    options_redq = False          # some

class renderfunc(stylefunc):
    """Parent class of all functions that produce rendertype content (text, math, code)"""
    # inputs (options and content)
    options_optl = True           # all
    options_redq = False          # all



###########################################
#          Settings Functions

class setContentStyle(settingsfunc):
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
    def validateOptions(string):
        pass

class setPageNumbers(settingsfunc):
    """Set page numbers (PDF only)"""
    def __new__(cls, doc: Document, 
                num_type="numbers", start_num=0, start_pg=1, evens_only=False):
        pass # TODO: pdf

class setOutput(settingsfunc):
    """Set the type and destination of Docupose rendering. Use extensions .pdf or .html for `name`."""
    def __new__(cls, doc: Document, 
                name="main", size="default"):
        pass # TODO

class setArgs(settingsfunc):
    """Set default arguments for the options of content functions."""
    def __new__(cls, doc: Document, func, **kwargs):
        pass



###########################################
#            Import Functions

class importPackage(importfunc):
    """Import a package into the namespace. Functions can be accessed with the @ operator."""
    def __new__(cls, doc: Document, 
                pkgLocation):
        pkgLocation
        doc.namespace[pkgLocation]

class importFrom(importfunc):
    """Import a specific function from a package."""
    def __new__(cls, doc: Document, objName, pkgName):
        pass

class importContent(importfunc):
    """Import text, math or code content from another file."""
    def __new__(cls, doc: Document, fileName, renderType="text"):
        pass



###########################################
#            RunCode Function

class runCode(execfunc):
    """Run python code that can access and adjust the namespace of the document."""
    def __new__(cls, doc: Document, content):
        pass



###########################################
#            Symbol Functions

class t(symbolfunc):
    """Add indent(s) or tab(s)."""
    receives_options = True
    unicode_int = 9
    def __new__(cls, doc: Document, num=1):
        pass

class s(symbolfunc):
    """Add space(s)."""
    receives_options = True
    unicode_int = 32
    def __new__(cls, doc: Document, num=1):
        pass

class newline(symbolfunc):
    """Add newline(s). 
    For convenience, it is recommended to use the shorthand instead: \\\\"""
    receives_options = True
    unicode_int = 10
    def __new__(cls, doc: Document, num=1):
        pass

class quotationmark(symbolfunc):
    """Add quotation mark (i.e., \"), with optional symbol type left (i.e., L) or right (i.e., R). 
    For convenience, it is recommended to use shorthands instead: \\\" for \\quotationmark, \\ql for \\quotationmark[L], or \\qr for \\quotationmark[R]"""
    receives_options = True
    unicode_int = {DEFAULT: 34, "L": 8220, "R": 8221}
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class ql(symbolfunc):
    """Add left (aka opening) quotation mark. Used as a shorthand for \\q[L]"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class qr(symbolfunc):
    """Add right (aka closing) quotation mark. Used as a shorthand for \\q[R]"""
    receives_options = False
    def __new__(cls, doc: Document, place=None):
        pass

class dollar(symbolfunc):
    """Add dollar sign (i.e., $). 
    For convenience, it is recommended to use the shorthand instead: \\$"""
    receives_options = False
    unicode_int = 36
    def __new__(cls, doc: Document, place=None):
        pass

class backtick(symbolfunc):
    """Add backtick (i.e., `). 
    For convenience, it is recommended to use the shorthand instead: \\`"""
    receives_options = False
    unicode_int = 96
    def __new__(cls, doc: Document, place=None):
        pass

class pipe(symbolfunc):
    """Add pipe (i.e., |). 
    For convenience, it is recommended to use the shorthand instead: \\|"""
    receives_options = False
    unicode_int = 124
    def __new__(cls, doc: Document):
        pass

class bracket(symbolfunc):
    """Add bracket (i.e., [ or ]) with symbol type left (i.e., L) or right (i.e., R). 
    For convenience, it is recommended to use shorthands instead: \\[ for \\bracket[L], or \\] for \\bracket[R]"""
    receives_options = True
    unicode_int = {DEFAULT: 91, "L": 91, "R": 93}
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class brace(symbolfunc):
    """Add brace (i.e., { or }) with symbol type left (i.e., L) or right (i.e., R). 
    For convenience, it is recommended to use shorthands instead: \\{ for \\brace[L], or \\} for \\brace[R]"""
    receives_options = True
    unicode_int = {DEFAULT: 123, "L": 123, "R": 125}
    def __new__(cls, doc: Document, symbol_type=None):
        pass

class at(symbolfunc):
    """Add at-symbol (i.e., @).
    For convenience, it is recommended to use the shorthand instead: \\@"""
    receives_options = False
    unicode_int = 64
    def __new__(cls, doc: Document, place=None):
        pass

class pound(symbolfunc):
    """Add pound (i.e., #).
    For convenience, it is recommended to use the shorthand instead: \\#"""
    receives_options = False
    unicode_int = 35
    def __new__(cls, doc: Document, place=None):
        pass

class percent(symbolfunc):
    """Add percent-symbol (i.e., %).
    For convenience, it is recommended to use the shorthand instead: \\%"""
    receives_options = False
    unicode_int = 37
    def __new__(cls, doc: Document):
        pass

class bang(symbolfunc):
    """Add exclamation mark (i.e., !).
    For convenience, it is recommended to use the shorthand instead: \\!"""
    receives_options = False
    unicode_int = 33
    def __new__(cls, doc: Document):
        pass

class dagger(symbolfunc):
    """Add a dagger (i.e., †)."""
    receives_options = False
    unicode_int = 8224
    def __new__(cls, doc: Document):
        pass

class ddagger(symbolfunc):
    """Add a double dagger (i.e., ‡)."""
    receives_options = False
    unicode_int = 8225
    def __new__(cls, doc: Document):
        pass

class ellipses(symbolfunc):
    """Add an ellipses (i.e., …)."""
    receives_options = False
    unicode_int = 8230
    def __new__(cls, doc: Document):
        pass

class arrow(symbolfunc):
    """Add an arrow (i.e., ↑, →, ←, ↓, ↔, ↕, ↖, ↗, ↘, ↙), with specified direction."""
    receives_options = True
    unicode_int = {'U': 8593, 'R': 8594, 'L': 8592, 'D': 8595, 
                   'UL': 8598, 'UR': 8599, 'DL': 8600, 'DR': 8601,
                   'LR': 8596, 'UD': 8597, DEFAULT: 8593}
    def __new__(cls, doc: Document):
        pass

class blockarrow(symbolfunc):
    """Add a block arrow (i.e., ⇦, ⇧, ⇨, ⇩), with specified direction."""
    receives_options = True
    unicode_int = {"L": 8678, "U": 8679, "R": 8680, "D": 8681, DEFAULT: 8680}
    def __new__(cls, doc: Document):
        pass

class dottedarrow(symbolfunc):
    """Add a dotted arrow (i.e., ⇠, ⇡, ⇢, ⇣), with specified direction."""
    receives_options = True
    unicode_int = {"L": 8672, "U": 8673, "R": 8674, "D": 8675, DEFAULT: 8674}
    def __new__(cls, doc: Document):
        pass

class doublearrow(symbolfunc):
    """Add a dotted arrow (i.e., ⇒, ⇐, ⇔, ⇕, ⇖, ⇗, ⇘, ⇙), with specified direction."""
    receives_options = True
    unicode_int = {"U": 8657, "D": 8659, "R": 8658, "L": 8656, 
                   "LR": 8660, "UD": 8661, 
                   "UL": 8662, "UR": 8663, "DR": 8664, "DL": 8665, DEFAULT: 8658}
    def __new__(cls, doc: Document):
        pass

class backforth(symbolfunc):
    """Add back-and-forth arrows (i.e., ⇆, ⇵, ⇋), with specified direction."""
    receives_options = True
    unicode_int = {DEFAULT: 8651, "LR": 8646, "UD": 8693}
    def __new__(cls, doc: Document):
        pass

class forthback(symbolfunc):
    """Add forth-and-back arrows (i.e., ⇄, ⇅, ⇌), with specified direction."""
    receives_options = True
    unicode_int = {DEFAULT: 8652, "LR": 8644, "UD": 8645}
    def __new__(cls, doc: Document):
        pass

class forall(symbolfunc):
    """Add mathematical 'for all' symbol (i.e., ∀)."""
    receives_options = False
    unicode_int = 8704
    def __new__(cls, doc: Document):
        pass

class partial(symbolfunc):
    """Add mathematical 'partial' symbol (i.e., ∂)."""
    receives_options = False
    unicode_int = 8706
    def __new__(cls, doc: Document):
        pass

class partial(symbolfunc):
    """Add mathematical 'partial' symbol (i.e., ∂)."""
    receives_options = False
    unicode_int = 8706
    def __new__(cls, doc: Document):
        pass

class exists(symbolfunc):
    """Add mathematical 'there exists' symbol (i.e., ∃)."""
    receives_options = False
    unicode_int = 8707
    def __new__(cls, doc: Document):
        pass

class nexists(symbolfunc):
    """Add mathematical 'there does not exists' symbol (i.e., ∄)."""
    receives_options = False
    unicode_int = 8708
    def __new__(cls, doc: Document):
        pass

class Delta(symbolfunc):
    """Add greek Delta symbol (i.e., ∆)."""
    receives_options = False
    unicode_int = 8710
    def __new__(cls, doc: Document):
        pass

class emptyset(symbolfunc):
    """Add mathematical 'empty set' symbol (i.e., ∅)."""
    receives_options = False
    unicode_int = 8709
    def __new__(cls, doc: Document):
        pass

class in_(symbolfunc):
    """Add mathematical 'in' symbol (i.e., ∈)."""
    receives_options = False
    unicode_int = 8712
    def __new__(cls, doc: Document):
        pass

class ni(symbolfunc):
    """Add mathematical 'in' symbol, leftward version (i.e., ∋)."""
    receives_options = False
    unicode_int = 8715
    def __new__(cls, doc: Document):
        pass

class nin(symbolfunc):
    """Add mathematical 'not in' symbol (i.e., ∉)."""
    receives_options = False
    unicode_int = 8713
    def __new__(cls, doc: Document):
        pass

class nni(symbolfunc):
    """Add mathematical 'not in' symbol, leftward version (i.e., ∌)."""
    receives_options = False
    unicode_int = 8716
    def __new__(cls, doc: Document):
        pass

class sum_(symbolfunc):
    """Add mathematical 'sum' symbol (i.e., ∑)."""
    receives_options = False
    unicode_int = 8721
    def __new__(cls, doc: Document):
        pass

class prod(symbolfunc):
    """Add mathematical 'product' symbol (i.e., ∏)."""
    receives_options = False
    unicode_int = 8719
    def __new__(cls, doc: Document):
        pass

class pm(symbolfunc):
    """Add mathematical 'plus-minus' symbol (i.e., ±)."""
    receives_options = False
    unicode_int = 177
    def __new__(cls, doc: Document):
        pass

class mp(symbolfunc):
    """Add mathematical 'plus-minus' symbol (i.e., ∓)."""
    receives_options = False
    unicode_int = 8723
    def __new__(cls, doc: Document):
        pass

class cdot(symbolfunc):
    """Add cender dot (i.e., ∙)."""
    receives_options = False
    unicode_int = 8729
    def __new__(cls, doc: Document):
        pass

class infty(symbolfunc):
    """Add mathematical 'infinity' symbol (i.e., ∞)."""
    receives_options = False
    unicode_int = 8734
    def __new__(cls, doc: Document):
        pass

class prop(symbolfunc):
    """Add mathematical 'proportional to' symbol (i.e., ∝)."""
    receives_options = False
    unicode_int = 8733
    def __new__(cls, doc: Document):
        pass

class sqrt(symbolfunc):
    """Add mathematical 'square root' symbol (i.e., √)."""
    receives_options = False
    unicode_int = 8730
    def __new__(cls, doc: Document):
        pass

class intercept(symbolfunc):
    """Add mathematical 'intercept' symbol (i.e., ∩)."""
    receives_options = False
    unicode_int = 8745
    def __new__(cls, doc: Document):
        pass

class union(symbolfunc):
    """Add mathematical 'union' symbol (i.e., ∪)."""
    receives_options = False
    unicode_int = 8746
    def __new__(cls, doc: Document):
        pass

class int_(symbolfunc):
    """Add mathematical 'integral' symbol (i.e., ∫)."""
    receives_options = False
    unicode_int = 8747
    def __new__(cls, doc: Document):
        pass

class doubleint(symbolfunc):
    """Add mathematical 'double integral' symbol (i.e., ∬)."""
    receives_options = False
    unicode_int = 8748
    def __new__(cls, doc: Document):
        pass

class tripleint(symbolfunc):
    """Add mathematical 'triple integral' symbol (i.e., ∭)."""
    receives_options = False
    unicode_int = 8749
    def __new__(cls, doc: Document):
        pass

class therefore(symbolfunc):
    """Add mathematical 'therefore' symbol (i.e., ∴)."""
    receives_options = False
    unicode_int = 8756
    def __new__(cls, doc: Document):
        pass

class approx(symbolfunc):
    """Add mathematical 'approximately' symbol (i.e., ≈)."""
    receives_options = False
    unicode_int = 8776
    def __new__(cls, doc: Document):
        pass

class napprox(symbolfunc):
    """Add mathematical 'not approximately' symbol (i.e., ≉)."""
    receives_options = False
    unicode_int = 8777
    def __new__(cls, doc: Document):
        pass

class implies(symbolfunc):
    """Add implies arrow (i.e., ⇒). Shortcut for \\doublearrow[R]."""
    receives_options = False
    def __new__(cls, doc: Document):
        pass

class impliedby(symbolfunc):
    """Add implied-by arrow (i.e., ⇐). Shortcut for \\doublearrow[L]."""
    receives_options = False
    def __new__(cls, doc: Document):
        pass

class iff(symbolfunc):
    """Add iff arrow (i.e., ⇔). Shortcut for \\doublearrow[LR]."""
    receives_options = False
    def __new__(cls, doc: Document):
        pass

class alpha(symbolfunc):
    """Add greek alpha letter (i.e., α)."""
    receives_options = False
    unicode_int = 945
    def __new__(cls, doc: Document):
        pass

class beta(symbolfunc):
    """Add greek beta letter (i.e., β)."""
    receives_options = False
    unicode_int = 946
    def __new__(cls, doc: Document):
        pass

class gamma(symbolfunc):
    """Add greek gamma letter (i.e., γ)."""
    receives_options = False
    unicode_int = 947
    def __new__(cls, doc: Document):
        pass

class delta(symbolfunc):
    """Add greek delta letter (i.e., δ)."""
    receives_options = False
    unicode_int = 948
    def __new__(cls, doc: Document):
        pass

class epsilon(symbolfunc):
    """Add greek epsilon letter (i.e., ε)."""
    receives_options = False
    unicode_int = 949
    def __new__(cls, doc: Document):
        pass

class zeta(symbolfunc):
    """Add greek zeta letter (i.e., ζ)."""
    receives_options = False
    unicode_int = 950
    def __new__(cls, doc: Document):
        pass

class eta(symbolfunc):
    """Add greek eta letter (i.e., η)."""
    receives_options = False
    unicode_int = 951
    def __new__(cls, doc: Document):
        pass

class theta(symbolfunc):
    """Add greek theta letter (i.e., θ)."""
    receives_options = False
    unicode_int = 952
    def __new__(cls, doc: Document):
        pass

class iota(symbolfunc):
    """Add greek iota letter (i.e., ι)."""
    receives_options = False
    unicode_int = 953
    def __new__(cls, doc: Document):
        pass

class kappa(symbolfunc):
    """Add greek kappa letter (i.e., κ)."""
    receives_options = False
    unicode_int = 954
    def __new__(cls, doc: Document):
        pass

class lambda_(symbolfunc):
    """Add greek lambda letter (i.e., λ)."""
    receives_options = False
    unicode_int = 955
    def __new__(cls, doc: Document):
        pass

class mu(symbolfunc):
    """Add greek mu letter (i.e., μ)."""
    receives_options = False
    unicode_int = 956
    def __new__(cls, doc: Document):
        pass

class nu(symbolfunc):
    """Add greek nu letter (i.e., ν)."""
    receives_options = False
    unicode_int = 957
    def __new__(cls, doc: Document):
        pass

class xi(symbolfunc):
    """Add greek xi letter (i.e., ξ)."""
    receives_options = False
    unicode_int = 958
    def __new__(cls, doc: Document):
        pass

class omicron(symbolfunc):
    """Add greek omicron letter (i.e., ο)."""
    receives_options = False
    unicode_int = 959
    def __new__(cls, doc: Document):
        pass

class pi(symbolfunc):
    """Add greek pi letter (i.e., π)."""
    receives_options = False
    unicode_int = 960
    def __new__(cls, doc: Document):
        pass

class rho(symbolfunc):
    """Add greek rho letter (i.e., ρ)."""
    receives_options = False
    unicode_int = 961
    def __new__(cls, doc: Document):
        pass

class sigma(symbolfunc):
    """Add greek sigma letter (i.e., σ)."""
    receives_options = False
    unicode_int = 963
    def __new__(cls, doc: Document):
        pass

class tau(symbolfunc):
    """Add greek tau letter (i.e., τ)."""
    receives_options = False
    unicode_int = 964
    def __new__(cls, doc: Document):
        pass

class upsilon(symbolfunc):
    """Add greek upsilon letter (i.e., υ)."""
    receives_options = False
    unicode_int = 965
    def __new__(cls, doc: Document):
        pass

class phi(symbolfunc):
    """Add greek phi letter (i.e., φ)."""
    receives_options = False
    unicode_int = 966
    def __new__(cls, doc: Document):
        pass

class chi(symbolfunc):
    """Add greek chi letter (i.e., χ)."""
    receives_options = False
    unicode_int = 967
    def __new__(cls, doc: Document):
        pass

class psi(symbolfunc):
    """Add greek psi letter (i.e., ψ)."""
    receives_options = False
    unicode_int = 968
    def __new__(cls, doc: Document):
        pass

class omega(symbolfunc):
    """Add greek omega letter (i.e., ω)."""
    receives_options = False
    unicode_int = 969
    def __new__(cls, doc: Document):
        pass

class Alpha(symbolfunc):
    """Add greek Alpha letter (i.e., Α)."""
    receives_options = False
    unicode_int = 913
    def __new__(cls, doc: Document):
        pass

class Beta(symbolfunc):
    """Add greek Beta letter (i.e., Β)."""
    receives_options = False
    unicode_int = 914
    def __new__(cls, doc: Document):
        pass

class Gamma(symbolfunc):
    """Add greek Gamma letter (i.e., Γ)."""
    receives_options = False
    unicode_int = 915
    def __new__(cls, doc: Document):
        pass

class Delta(symbolfunc):
    """Add greek Delta letter (i.e., Δ)."""
    receives_options = False
    unicode_int = 916
    def __new__(cls, doc: Document):
        pass

class Epsilon(symbolfunc):
    """Add greek Epsilon letter (i.e., Ε)."""
    receives_options = False
    unicode_int = 917
    def __new__(cls, doc: Document):
        pass

class Zeta(symbolfunc):
    """Add greek Zeta letter (i.e., Ζ)."""
    receives_options = False
    unicode_int = 918
    def __new__(cls, doc: Document):
        pass

class Eta(symbolfunc):
    """Add greek Eta letter (i.e., Η)."""
    receives_options = False
    unicode_int = 919
    def __new__(cls, doc: Document):
        pass

class Theta(symbolfunc):
    """Add greek Theta letter (i.e., Θ)."""
    receives_options = False
    unicode_int = 920
    def __new__(cls, doc: Document):
        pass

class Iota(symbolfunc):
    """Add greek Iota letter (i.e., Ι)."""
    receives_options = False
    unicode_int = 921
    def __new__(cls, doc: Document):
        pass

class Kappa(symbolfunc):
    """Add greek Kappa letter (i.e., Κ)."""
    receives_options = False
    unicode_int = 922
    def __new__(cls, doc: Document):
        pass

class Lambda(symbolfunc):
    """Add greek Lambda letter (i.e., Λ)."""
    receives_options = False
    unicode_int = 923
    def __new__(cls, doc: Document):
        pass

class Mu(symbolfunc):
    """Add greek Mu letter (i.e., Μ)."""
    receives_options = False
    unicode_int = 924
    def __new__(cls, doc: Document):
        pass

class Nu(symbolfunc):
    """Add greek Nu letter (i.e., Ν)."""
    receives_options = False
    unicode_int = 925
    def __new__(cls, doc: Document):
        pass

class Xi(symbolfunc):
    """Add greek Xi letter (i.e., Ξ)."""
    receives_options = False
    unicode_int = 926
    def __new__(cls, doc: Document):
        pass

class Omicron(symbolfunc):
    """Add greek Omicron letter (i.e., Ο)."""
    receives_options = False
    unicode_int = 927
    def __new__(cls, doc: Document):
        pass

class Pi(symbolfunc):
    """Add greek Pi letter (i.e., Π)."""
    receives_options = False
    unicode_int = 928
    def __new__(cls, doc: Document):
        pass

class Rho(symbolfunc):
    """Add greek Rho letter (i.e., Ρ)."""
    receives_options = False
    unicode_int = 929
    def __new__(cls, doc: Document):
        pass

class Sigma(symbolfunc):
    """Add greek Sigma letter (i.e., Σ)."""
    receives_options = False
    unicode_int = 931
    def __new__(cls, doc: Document):
        pass

class Tau(symbolfunc):
    """Add greek Tau letter (i.e., Τ)."""
    receives_options = False
    unicode_int = 932
    def __new__(cls, doc: Document):
        pass

class Upsilon(symbolfunc):
    """Add greek Upsilon letter (i.e., Υ)."""
    receives_options = False
    unicode_int = 933
    def __new__(cls, doc: Document):
        pass

class Phi(symbolfunc):
    """Add greek Phi letter (i.e., Φ)."""
    receives_options = False
    unicode_int = 934
    def __new__(cls, doc: Document):
        pass

class Chi(symbolfunc):
    """Add greek Chi letter (i.e., Χ)."""
    receives_options = False
    unicode_int = 935
    def __new__(cls, doc: Document):
        pass

class Psi(symbolfunc):
    """Add greek Psi letter (i.e., Ψ)."""
    receives_options = False
    unicode_int = 936
    def __new__(cls, doc: Document):
        pass

class Omega(symbolfunc):
    """Add greek Omega letter (i.e., Ω)."""
    receives_options = False
    unicode_int = 937
    def __new__(cls, doc: Document):
        pass




###########################################
#             Style Functions

class empf(stylefunc):
    """Set emphasis for content"""
    options_optl = False
    options_redq = True
    def __new__(cls, doc: Document, content):
        pass

class bo(stylefunc):
    """Bold textlike content"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class it(stylefunc):
    """Italicize textlike content"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class un(stylefunc):
    """Underline textlike content"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class ef(stylefunc):
    """Remove all emphasis from textlike content"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class columns(stylefunc):
    """Set content into columns"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class columnbreak(stylefunc):
    """Break content between columns while using \\columns"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class list(stylefunc):
    """Make list of content"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class framed(stylefunc):
    """Put frame around content"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class quote(stylefunc):
    """Format content as quotation"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class color(stylefunc):
    """Set color for textlike content"""
    options_optl = False
    options_redq = True
    def __new__(cls, doc: Document, content):
        pass

class strike(stylefunc):
    """Set strike through content"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class smallcaps(stylefunc):
    """Set all textlike content to smallcaps"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class align(stylefunc):
    """Set alignment for any content"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class center(stylefunc):
    """Set alignment for any content. Shorthand for \\align[C]"""
    options_optl = False
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass



###########################################
#          Reference Functions

class title(reffunc):
    """Create a title for the document. Can be referenced with \\contents or elsewhere in doc."""
    options_redq = False
    def __new__(cls, doc: Document, *content):
        pass

class section(reffunc):
    """Create a section for the document. Can be referenced with \\contents or elsewhere in doc."""
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class subsection(reffunc):
    """Create a subsection for the document. Can be referenced with \\contents or elsewhere in doc."""
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class caption(reffunc):
    """Create a caption for content. Can be referenced with \\contents or elsewhere in doc."""
    options_redq = True
    def __new__(cls, doc: Document, content):
        pass

class footnote(reffunc):
    """Create a footnote for content. Can be referenced with \\citations or elsewhere in doc."""
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class contents(reffunc):
    """Create a table of contents for the document. Uses references."""
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class citations(reffunc):
    """Create a citation list or bibliography."""
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass



###########################################
#             Render Functions

class text(renderfunc):
    """Create content with rendertype 'text'. 
    For clarity, it is recommended to use text render gates (i.e., \"\")"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class math(renderfunc):
    """Create content with rendertype 'math'.
    For clarity, it is recommended to use math render gates (i.e., $$)"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass

class code(renderfunc):
    """Create content with rendertype 'code'.
    For clarity, it is recommended to use code render gates (i.e., ``)"""
    options_optl = True
    options_redq = False
    def __new__(cls, doc: Document, content):
        pass



###########################################
#             Image Function

class image(figfunc):
    def __new__(cls, doc: Document, content):
        pass



###########################################
#  Single-Char Symbol Function Shorthands

symbol_shorthands =  {
    "\"": "quotationmark",      # replace  \"  with  \quotationmark
    "\\": "newline",            # replace  \\  with  \newline
    "_": "underscore",          # replace  \_  with  \underscore
    "^": "carrot",              # replace  \^  with  \carrot
    "$": "dollar",              # replace  \$  with  \dollar
    "`": "backtick",            # replace  \`  with  \backtick
    "|": "pipe",                # replace  \|  with  \pipe
    "[": "bracket[L]",          # replace  \[  with  \bracket[L]
    "]": "bracket[R]",          # replace  \]  with  \bracket[R]
    "{": "brace[L]",            # replace  \{  with  \brace[L]
    "}": "brace[R]",            # replace  \}  with  \brace[R]
    "@": "atsymbol",            # replace  \@  with  \atatsymbol
    "#": "pound",               # replace  \#  with  \pound
    "%": "percent",             # replace  \%  with  \percent
    "!": "bang",                # replace  \%  with  \bang
}



###########################################
#            Function Namespace

default_namespace = {}
local_namespace = locals().copy()
for string, obj in local_namespace.items():
    if isinstance(obj, type) and issubclass(obj, dpfunc) and string[0].islower(): # TODO: fix lower
        default_namespace[f"\\{string.replace('_', '')}"] = obj
