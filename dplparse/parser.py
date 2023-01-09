from syntax import ministr_gate_regex, enclosers_regex, open_enclosers_regex, next_func_regex
from syntax import option_lids, content_lids, open_lids, close_lids
from syntax import all_gates, ministr_gate
from dptypes import getDPType, getDPLiteral, getDPFunc
from typecheck import checkType, Num
from sys import exit
import re



############################################
#              parsing classes

class parse_str:
    def __init__(self, string, line_s=None, col_s=None, col_e=None, line_e=None):
        line_e = None if line_s == line_e else line_e
        if any(param is None for param in (line_s, col_s, col_e)):
            line_s = col_s = 0
            lines = string.split("\n")
            line_e = len(lines) - 1
            line_e = None if line_s == line_e else line_e
            col_e = len(lines[-1])
        if not isinstance(string, str) or \
           not all(isinstance(i, int) for i in (line_s, col_s, col_e)) or \
           not (isinstance(line_e, int) or line_e is None) or \
           (line_e is None and (col_e < col_s or any(i < 0 for i in (line_s, col_s, col_e)))) or \
           (line_e is not None and (line_e < line_s or any(i < 0 for i in (line_s, col_s, col_e, line_e)))):
            raise TypeError("Bad input.")
        elif (line_e is None and string.count("\n")) or \
           (line_e is not None and string.count("\n") != line_e - line_s):
            raise TypeError("Number of lines of string must match indices.")
        elif (line_e is None and len(string) != col_e - col_s) or \
             (line_e is not None and len(string.split("\n")[-1]) != col_e):
            raise TypeError("Number of characters of string must match indices.")
        self.string = string
        line_e = line_s if line_e is None else line_e
        self.line_s = line_s
        self.line_e = line_e
        self.col_s = col_s
        self.col_e = col_e
    
    def _getLinesDict(self):
        return dict(zip(range(self.line_s, self.line_e + 1), self.string.split("\n")))
    
    def nextChr(self, obj):
        if isinstance(obj, parse_str) and obj in self:
            end = self._getIndices(obj)[1]
            return self[end]
    
    def following(self, obj):
        if isinstance(obj, parse_str) and obj in self:
            end = self._getIndices(obj)[1]
            return self[end:]

    def count(self, pattern, regex=True):
        if not regex:
            pattern = re.escape(pattern)
        return len(re.findall(pattern, self.string))
    
    def get(self, line_s, col_s, col_e, line_e=None):
        if (line_e is None and (col_s < self.col_s or col_e > self.col_e or line_s != self.line_s)) or \
           (line_e is not None and ((line_s < self.line_s or line_e > self.line_e) or \
                                    (line_s == self.line_s and col_s < self.col_s) or \
                                    (line_e == self.line_e and col_e > self.col_e))):
            raise TypeError("Bad indices: indices outside of possible ranges.")
        lines = self._getLinesDict()
        line_e = line_s if line_e is None else line_e
        if (line_s == self.line_s and len(lines[line_s]) + self.col_s < col_s) or \
           (line_s > self.line_s and len(lines[line_s]) < col_s) or \
           (line_e < self.line_e and len(lines[line_e]) < col_e):
            raise TypeError("Bad indices: column index passes number of line characters.")
        lines = {key: value for key, value in lines.items() if line_s <= key <= line_e}
        lines[line_e] = lines[line_e][:col_e]
        if self.line_s == line_s:
            lines[line_s] = lines[line_s][col_s - self.col_s:]
        else:
            lines[line_s] = lines[line_s][col_s:]
        return parse_str("\n".join(lines.values()), line_s, col_s, col_e, line_e)
    
    def match(self, pattern, regex=True):
        if not regex:
            pattern = re.escape(pattern)
        return self._processMatch(re.match(pattern, self.string))

    def search(self, pattern, regex=True):
        if not regex:
            pattern = re.escape(pattern)
        return self._processMatch(re.search(pattern, self.string))
    
    def finditer(self, pattern, regex=True):
        if not regex:
            pattern = re.escape(pattern)
        return map(self._processMatch, re.finditer(pattern, self.string))
    
    def split(self, pattern, regex=True):
        if not regex:
            pattern = re.escape(pattern)
        matches = tuple(self.finditer(pattern))
        if not matches:
            return [self]
        final = []
        line_s = self.line_s
        col_s = self.col_s
        col_e = None
        line_e = None
        for delim in matches:
            col_e = delim.col_s
            line_e = delim.line_s
            final.append(self.get(line_s, col_s, col_e, line_e))
            line_s = delim.line_e
            col_s = delim.col_e
        final.append(self.get(line_s, col_s, self.col_e, self.line_e))
        return final

    def strip(self):
        return self._processMatch(re.search("(?<=\s)\S.+\S(?=\s)", self.string, re.DOTALL))
    
    def getRange(self, start, end=None):
        if isinstance(start, parse_str):
            if isinstance(end, parse_str):
                start_indx = self._getIndices(start)[0]
                end_indx = self._getIndices(end)[1]
                return self[start_indx:end_indx]
            elif end == None:
                return start
    
    def _getIndices(self, obj, regex=False):
        if isinstance(obj, str):
            if not regex:
                obj = re.escape(obj)
            match = re.search(obj, self.string)
            return match.span()
        if isinstance(obj, parse_str) and obj in self:
            if obj.line_s == self.line_s:
                start = obj.col_s - self.col_s
            else:
                lines = {num: len(line) + 1 for num, line in self._getLinesDict().items()}
                start = sum(lines[linenum] for linenum in range(self.line_s, obj.line_s)) + obj.col_s
            end = start + len(obj.string)
            return (start, end)
        else:
            return None

    def _processMatch(self, match):
        if isinstance(match, re.Match):
            match = {"string": match[0], "start": match.start()}
        if match:
            mstring = match["string"]
            if mstring == self.string:
                return self
            # prematch and starting indices
            prematch_lst = self.string[:match["start"]].split("\n")
            mline_s = self.line_s + len(prematch_lst) - 1
            mcol_s = len(prematch_lst[-1]) + (self.col_s if len(prematch_lst) == 1 else 0)
            # match and end incices
            match_lst = mstring.split("\n")
            mline_e = mline_s + len(match_lst) - 1
            mcol_e = len(match_lst[-1]) + (mcol_s if mline_e == mline_s else 0)
            return parse_str(mstring, mline_s, mcol_s, mcol_e, mline_e)
        else:
            return None
    
    def __str__(self):
        return self.string
    
    def __contains__(self, item):
        if isinstance(item, parse_str):
            return item.string == self.get(item.line_s, item.col_s, item.col_e, item.line_e).string
        elif isinstance(item, str):
            return item in self.string
    
    def __getitem__(self, obj):
        if isinstance(obj, int):
            obj += len(self.string) if obj < 0 else 0
            if 0 <= obj < len(self.string):
                obj = slice(obj, obj + 1)
        if isinstance(obj, slice):
            start, end = obj.start, obj.stop
            if start == None:
                start = 0
            else:
                start += len(self.string) if start < 0 else 0
            if end == None:
                end = len(self.string)
            else:
                end += len(self.string) if end < 0 else 0
            if 0 <= start <= end <= len(self.string):   
                return self._processMatch({"string": self.string[start:end], "start": start})
        return None
    
    def __bool__(self):
        return bool(self.string)
    
    def __add__(self, obj):
        if isinstance(obj, parse_str) and self.line_e == obj.line_s and self.col_e == obj.col_s:
            return parse_str(self.string + obj.string, self.line_s, self.col_s, obj.col_e, obj.line_s)

class dpparser(parse_str):
    MISSING_OPENER, MISSING_CLOSER, MISPLACED_CLOSER = range(3)
    dpeval = None
    options = None
    content = None
    def getFuncLst(self, namespace, lines):
        remaining = self
        func_lst = []
        while func := remaining.search(next_func_regex):
            char = remaining.nextChr(func)
            end = None
            if char.string == option_lids[0]:
                options = remaining.getEnclosed(char)
                end = options
                char = remaining.nextChr(options)
            if char.string == content_lids[0]:
                content = remaining.getEnclosed(char)
                end = content
            new_func = self.getRange(func, end)
            if isinstance(new_func, dpparser) and new_func in namespace:
                new_func.dpeval = getDPFunc(new_func.string, namespace)
            else:
                pass # TODO raise error

    def getEnclosed(self, start_obj=None, regex=True):
        # find opener if none specified
        if start_obj == None:
            start_obj = self.search(open_enclosers_regex)
            if start_obj == None:
                return self.MISSING_OPENER
        # convert start_obj to parse_str
        if isinstance(start_obj, str):
            start_obj = self.search(start_obj, regex)
        # process start_obj
        if isinstance(start_obj, parse_str) and start_obj in self:
            enclosers_lst = [start_obj.string]
            start, end = self._getIndices(start_obj)
            while enclosers_lst:
                search_regex = ministr_gate_regex \
                                if enclosers_lst[-1] == ministr_gate \
                                else enclosers_regex
                match = self[end:].search(search_regex)
                if not match:
                    return self.MISSING_CLOSER
                elif any(sym == match.string for sym in all_gates + (ministr_gate,)):
                    enclosers_lst.pop() if enclosers_lst[-1] == match.string else enclosers_lst.append(match.string)
                elif any(sym == match.string for sym in open_lids):
                    enclosers_lst.append(match.string)
                elif any(sym == match.string for sym in close_lids):
                    open_lid = option_lids[0] if match.string == option_lids[1] else content_lids[0]
                    if enclosers_lst[-1] == open_lid:
                        enclosers_lst.pop()
                    else:
                        return self.MISPLACED_CLOSER
                if not enclosers_lst:
                    end = self._getIndices(match)[1]
                    return self[start, end]
        else:
            return None
                
    def getSepdEntries(self, start_obj=None, regex=True):
        # convert start_obj to parse_str
        enclosed = self.getEnclosed(start_obj, regex)
        # process start_obj
        if isinstance(enclosed, parse_str) and start_obj in self:
            enclosers_lst = [start_obj.string]
            start, end = self._getIndices(start_obj)
            while enclosers_lst:
                search_regex = 
        else:
            return enclosed

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

