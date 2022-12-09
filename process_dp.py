
TEXT = 0
MATH = 1
CODE = 2


class Snip:
    def __init__(self, content, snip_type=TEXT, options=None):
        if not isinstance(content, str):
            raise TypeError("Content of snip must be string.") # TODO
        self.content = content
        self.snip_type = snip_type
        self.options = options
    
    def __len__(self):
        return len(self.content) # TODO

    def __add__(self, other):
        if isinstance(other, Snip):
            if self.snip_type == other.snip_type and \
                (not other.options or self.options == other.options):
                return Snip(
                    self.content + other.content, 
                    snip_type = self.snip_type
                )
            else:
                [self, other]
        else:
            raise TypeError(f"Cannot add snips of different types") # TODO
    
    def __mul__(self, other):
        if isinstance(other, int):
            return Snip(
                self.content * other,
                snip_type = self.snip_type,
                options = self.options
            )
        else:
            raise TypeError(f"Cannot multiply snip with non-integer") # TODO




