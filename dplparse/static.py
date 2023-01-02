doc_settings = {
    # render info
    "render": {
        "type": "html",
        "destination": None,
        "page_size": None,
    },
    
    # misc page details
    "page_nums": None,
    "page_bg": None,

    # margins
    "margin": {
        "L": 1,
        "R": 1,
        "T": 1,
        "B": 1,
    },

    # text settings
    "text": {
        "font": "default",
        "size": 12,
        "color": "#000000",
    },

    # math settings
    "math": {
        "font": "default",
        "size": 12,
        "color": "#000000",
    },

    # code settings
    "code": {
        "font": "default",
        "size": 12,
        "color": "#000000",
        "bg-color": "#999999",
        "border-width": 0,
        "border-radius": 3,
    },
}

doc_content = {
    "header": None,
    "footer": None,
    "body": None,
}

symbol_shorthands =  {
    "\\\"": "\\quotationmark",      # replace  \"  with  \quotationmark
    "\\\\": "\\newline",            # replace  \\  with  \newline
    "\\_": "\\underscore",          # replace  \_  with  \underscore
    "\\^": "\\carrot",              # replace  \^  with  \carrot
    "\\$": "\\dollar",              # replace  \$  with  \dollar
    "\\`": "\\backtick",            # replace  \`  with  \backtick
    "\\|": "\\pipe",                # replace  \|  with  \pipe
    "\\[": "\\bracket[O]",          # replace  \[  with  \bracket[O]
    "\\]": "\\bracket[C]",          # replace  \]  with  \bracket[C]
    "\\{": "\\brace[O]",            # replace  \{  with  \brace[O]
    "\\}": "\\brace[C]",            # replace  \}  with  \brace[C]
    "\\@": "\\atsymbol",            # replace  \@  with  \atatsymbol
    "\\#": "\\pound",               # replace  \#  with  \pound
}

types = (
    "display",
    "direction",
    "position",
    "symboltype",
    "rendertype",
    "imagetype",
    "grouptype",
    "nonetype",
    "color",
    "bool",
    "int",
    "float",
    "array",
    "ministr",
)

keywords = {
    # display
    "Inline": "display",
    "Block": "display",
    "InlineBlock": "display",
    "Full": "display",
    # directions
    "N": "direction",
    "S": "direction",
    "E": "direction",
    "W": "direction",
    "NE": "direction",
    "NW": "direction",
    "SE": "direction",
    "SW": "direction",
    # positions
    "L": "position",
    "T": "position",
    "R": "position",
    "B": "position",
    "M": "position",
    "TL": "position",
    "TR": "position",
    "BL": "position",
    "BR": "position",
    "ML": "position",
    "MR": "position",
    # symboltypes
    "O": "symboltype",
    "C": "symboltype",
    # rendertypes
    "text": "rendertype",
    "math": "rendertype",
    "code": "rendertype",
    # imagetype
    "image": "imagetype",
    "graphic": "imagetype",
    # Nonetypes
    "None": "nonetype",
    # bools
    "True": "bool",
    "False": "bool",
}

math_symbols = (
)

