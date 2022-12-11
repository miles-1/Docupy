<!-- https://upmath.me/ to convert to html-->

<style>
    body {
        font-family: 'Segoe UI';
        background: #1E1E1E;
        color: #D4D4D4;
    }
    code {
        color: yellow;
    }
    .rb {
        color: #4EC9B0;
    }
    .cmd {
        color: #569CD6;
    }
    .op {
        color: #FF8ED2;
    }
    .ct {
        color: #DA70D6;
    }
    .pl {
        color: #FFD700;
    }
    .comment {
        color: #57A64A;
        font-style: italic;
    }
</style>


<hr>


# Docupy, a typesetting script language

*Miles Robertson, 12/10/22*

<br>
<hr>
<br>

## Intro

**Docupy** is a tex-like, function-based typesetting script language that implements the following features:

- in-document python scripting for content generation
- user-defined variables and functions
- novice-friendly error messages
- simplified, template-free syntax with reduced need package imports
- exporting to HTML and PDF

<br>
<hr>
<br>

## Examples



### Text, Math and Code Rendering

Math rendering in Docupy is very similar to that seen in Latex, with a few changes to make syntax more consistent.

<pre style="font-family:consolas">
<span class="rb">"</span>The sum of the first <span class="rb">$</span>n<span class="rb">$</span> integers is <span class="rb">"</span> <span class="comment"># single " denotes inline text snip </span>
<span class="rb">$</span><span class="cmd">\sum</span><span class="pl">_</span>i<span class="pl">^</span>n i = <span class="cmd">\frac</span><span class="ct">{</span>n(n-1) <span class="ct">|</span> 2<span class="ct">}</span>.<span class="rb">$</span> <span class="comment"># single $ denotes inline math snip </span>
<span class="cmd">\hline</span> <span class="comment"># horizontal line</span>
<span class="rb">$$</span><span class="cmd">\cos</span>(<span class="cmd">\frac</span><span class="ct">{</span><span class="cmd">\pi</span> <span class="ct">|</span> 2<span class="ct">}</span>) = 0<span class="rb">$$</span> <span class="comment"># double $ denotes block math snip </span>
<span class="rb">""</span>A trig identity.<span class="rb">""</span> <span class="comment"># double " denotes block text snip </span>
<span class="cmd">\hline</span>
<span class="rb">`</span>myVar = 5<span class="rb">`</span> <span class="comment"># single ` denotes inline code snip </span>
</pre>

> <br><span style="font-family:times">The sum of the first</span> $n$ <span style="font-family:times">integers is</span>
> $\sum_i^n i = \frac{n(n-1)}{2}$.
> <hr>
>
> $$\cos \Big(\frac{\pi}{2} \Big) = 0$$
> <p style="font-family:times;text-align: center;">A trig identity.</p>
> <hr>
>
> `myVar = 5`
>
> <br>

<br>
<br>
<hr>
<br>

## Structure and Syntax

### Snips, Groups and Render Types

   - Conceptually, the basic unit of document content is a **snip**. This can be a paragraph of text, a math equation, a code snippet, an image, etc. 
   - **Render types** describe the class of snip (e.g., image, text, graphic, etc.). A snip can only have a single render type. 
   - Multiple snips may be contained within a **group**. Groups and spips alike can get "packed" or "gridded" into the document during rendering.

### Render Brackets for Text-Like Render Types
   - There are three **text-like render types** in Docupy: <span style="font-family:times;font-size:18px">text</span>, $math$ and <span style="font-family:consolas;font-size:16px;background:#CACACA;color:black;border-radius:5px;padding-left:4px;padding-right:4px;">code</span>. Each of these 
     have associated **render brackets**, listed below, that are used to set the content's render type. All typed text must be inside one of these render brackets to show up on the document. Nesting of render brackets is allowed.
       - `"abc"` for <span style="font-family:times;font-size:18px">text</span> rendering
       - `$abc$` for $math$ rendering
       - `` `abc` `` for <span style="font-family:consolas;font-size:16px;background:#CACACA;color:black;border-radius:5px;padding-left:4px;padding-right:4px;">code</span> rendering

### Basic `.dp` Rules

   - **Docupy renders `.dp` files**, which are plain text documents, to `.html` *(default)* or `.pdf`.
   - Documents require **no special structure** to set type onto the produced document (such as tex's `\begin{document}...\end{document}` or HTML's `<html>...</html>`).
   - Multiple **spaces** are treated as a single space by Docupy wherever they are found in `.dp` files. More spaces in content can be added by using `\s`&nbsp;. Likewise, multiple **new lines** between lines of code are changed to single new lines in `.dp` files, but in addition, are completely removed from any content. New lines in content can be added by using `\\`&nbsp;.
   - `.dp` files consist of a series of commands. These commands perform one of the following:
      - **Content Rendering**: this command type places content onto the rendered document. <!-- (or, as said [above](#snips-and-boxes), they *pack groups* into the document). -->
      - **Content Setup**: this command type prepares content to be rendered later. This can include changing the document format, setting variables, running Python code, etc.

### Namespace, Variables and Assignment

   - Names of variables and functions have the same rules as Python does, except underscores are not allowed. All names must be preceded with a `\`.
   - Assignment is done with the assignment operator: `<-`&nbsp;. The assignment operator "silences" the output of the code on the right of it (i.e., keeps if from being rendered to the document), and instead stores its output into the variable to be used later.
   - Users can define **variables** outside of render brackets. For example, the following line 
     would save the snip $a_c$ to the variable `\myVar`&nbsp;: 
     
     `\myVar <- $a_c$`

     After this line, `myVar` is added to the namespace of the document and can be used inside render brackets. Thus, for this line of code...

     `"The value of \myVar is small."`
     
     ... Docupy would render the following:

     > <span style="font-family:times;font-size:16px">The value of </span> $a_c$ <span style="font-family:times;font-size:16px">is small.</span>

### Functions

   - **Functions** can be called outside or inside of render brackets, and produce a snip as output.
   
   - There are two types of arguments that can be passed to functions: **options** (passed with `[]`) and **content** (passed with `{}`). Arguments are separated using `|`, whether or not it is within render brackets. For example, the following two lines of code...

     `\list[marker='right_tri' | size=12px]{"Option 1 | Option 2 | Option 3"}`
     
     `"\list[marker='right_tri' | size=12px]{Option 1 | Option 2 | Option 3}"`

     ... would both equivalently render as:

     > <span style="font-family:times;font-size:12px">▸ Option 1</span></br>
     > <span style="font-family:times;font-size:12px">▸ Option 2</span></br>
     > <span style="font-family:times;font-size:12px">▸ Option 3</span>

       - The *option* argumenmts allow users to specify visual properties of the output. Option arguments are often not required to use since they usually have defaults, but these defaults can be overwritten by using the form `optionsArgument=[new value here]`. 
       - The *content* arguments are often text-like, or sometimes include several lines of code. Either way, content arguments will produce some output that the function then processes. If content arguments are used, then the 
    
   - If a function requires no options (or arguments) when it is being called, the `[]` (or the `{}`) can be omitted or included with no difference in result.

   - Technically, in Docupy, *variables are functions with no arguments* that return content.

### Arrays

   - **Arrays** in Docupy are ordered collections of content, and have a fixed length. Generally, arrays are defined using `[]` around and as follows:
   
     `[\myVar | "second entry" | $K^2$]`

     However, if an array contains only text-like content of the same render type, then the two following lines define two equivalent arrays, the second a shorthand for the first:
    
     `[$a_k$ | $b_k$ | $c_k$]`

     `$a_k | b_k | c_k$`

 - If an array is passed to a function in `{}`, then each element in the array is interpreted as a separate argument. This means that the following three lines of code produce the same result, which is shown below:

     `"\list{Option 1 | Option 2 | Option 3}"`

     `\list{"Option 1 | Option 2 | Option 3"}`

     `\list{["Option 1" | "Option 2" | "Option 3"]}`

     > <span style="font-family:times">- Option 1</span></br>
     > <span style="font-family:times">- Option 2</span></br>
     > <span style="font-family:times">- Option 3</span>
   
- In cases where two-dimensional arrays are useful, such as matrices or tables, then rows within render brackets can be separated with `\\`. Thus, all of the following produce identical two-dimensional arrays (though the second is not recommended as it mixes the two syntaxes and is therefore somewhat confusing):

     `[[$a$ | $b$] | [$c$ | $d$]]`

     `[$a | b$ | $c | d$]`

     `$a | b \\ c | d$`
- Arrays can be indexed using `[]`.  For example, the code below would return $b_k$ :

    `[$a_k$ | $b_k$ | $c_k$][1]`

### Display settings and More on Rendering Brackets

- Snips or groups of snips can have different display settings, e.g., to keep within the line of text, or to break out into the next available space below, etc. The possible `display` values are `Inline`, `Block`, `Inline-Block` and `Full`, the first three being from HTML and the last indicating that the snip or group will be placed with full width and block display on the next page.
- For text-like render types, some of these display settings can be set using the corresponding render bracket multiple times:
    - Single use for `Inline` (e.g., `"hello this is inline"`)
    - Double use for `Block` (e.g., `$$y=mx+b$$`)
    - Triple use for `Full` (e.g., ` ```code goes here``` `)
- Alternatively, `display` values (along with font settings) can also be set using the option argument notation: `[display=InlineBlock | fontSize=]`

<br>
<hr>
<br>

## Default Namespace

Below is a list of functions (and their uses) that populate the namespace by default. This will likely change and increase during development. If an option argument is optional, its default value is indicated using `=`. If multiple content arguments are possible, the argument name is preceded by a `*`.

- `\\`&nbsp;: Add new line character. This ends the current line of text (if applicable) and adds a gap below the content. 

    *Option arguments: `[gapSize=1]`. No content arguments.*

- `\t`&nbsp;: Add tab (or horizontal space). This adds a horizontal space. 

    *Option arguments: `[gapSize=1]`. No content arguments.*

- `\title`&nbsp;: Adds title to document. 

    *Option arguments: `[size=16px | align=Center]`. Content arguments: `{title | *subtitles}`.*

- `\section`&nbsp;: Adds a section header. Name and ocurring page automatically logged for `\contents` function. 

    *Option arguments: `[size=14px | number=None | align=Center]`. Content arguments: `{title | *subtitles}`.*

- `\subsection`&nbsp;: Adds a subsection header. Name and ocurring page automatically logged for `\contents` function.

    *Option arguments: `[size=14px | number=None | align=Center]`. Content arguments: `{title | *subtitles}`.*

- `\columns`&nbsp;: Breaks content argument into multiple columns. `\columnbreak` is required inside of content.

    *Option arguments: `[num=2 | hAlign=Up | ratios=[1|1]]`. Content arguments: `{content}`.*

- `\columnbreak`&nbsp;: Specifies where column break should be.

    *No option or content arguments.*

- `\image`&nbsp;: Include an image. *Note:* `path` argument must use text render brackets `""`.

    *Option arguments: `[scale=1 | vAlign=Center]`. Content arguments: `{path}`*

- `\pack`&nbsp;: Specify the size and placement of the content.

    *Option arguments: `[width=1 | height=1 | allowPageBreak=True | borderWidth=0 | borderColor=0 | margin=0 | padding=0 | packAlign=Left | contentAlign=Left]`. Content arguments: `{content}`.*

- `\group`&nbsp;: Used to collect several snips into one group. Allows size specification, and used for subscripting functions.

    *Option arguments: `[width=1 | height=1 | allowPageBreak=True | borderWidth=0 | borderColor=0 | margin=0 | padding=0 | groupAlign=Left | contentAlign=Left]`. Content arguments: `{content}`.*

- `\caption`&nbsp;: Used as a subscript to `\group`, `\image` or other content to add a caption.

    *Option arguments: `[caption='Fig' | number=True | bold=True]`. Content arguments: `{caption}`.*

- `\transpose`&nbsp;: Get the transpose of a two-dimensional array.

    *Option arguments: `[array]`. No content arguments.*

- `\runCode`&nbsp;: Run pure python code inside of this command. Any python scripting has complete read/write access to document namespace by dropping the `\` before each name. *Note:* any variables in the python code with underscores are converted to camel case in the document namespace, possibly over-writing other variables if poorly named.

    *Option arguments: `[render=False]`. Content arguments: `{content}`.*

<br>
<hr>
<br>

## Data Types

### Basic Types
These data types are most often used in option arguments. Most of them are rarely used elsewhere.
- `bool`: Python boolean. Either `True` or `False`.
- `int`: Python integer.
- `float`: Python float.
- `position`: Indicates relative positioning. One of the following:
    - `N`, `S`, `E`, `W`, `NE`, `NW`, `SE`, `SW`.
    - `Left`, `South`, `Up`, `Down`, `Center` or their first letters.
- `color`: Color value in the form of hexadecimal. 
    - Written in the form `+000000`. 
    - Make `color` from `int`s using `\hexColor` function.
- `display`: HTML-like display values. One of the following:
    - `Inline`, `Block`, `InlineBlock`, `Full`
- `array`: One- or two-dimensional array as defined above.
- `ministr`: Short fragment of text, often for caption formatting. Can be any length, but not meant to be long. Denoted by `''`.
    - Examples: `'Fig'`, `'Table'`, `'Graph'`, etc.
- `nonetype`: The type of `None`.

### Render Types
Below, all but `group` are types of snips.
- `text`: <span style="font-family:times;font-size:18px">text</span> content. Make with `""` render brackets.
- `math`: $math$ content. Make with `$$` render brackets.
- `code`: <span style="font-family:consolas;font-size:16px;background:#CACACA;color:black;border-radius:5px;padding-left:4px;padding-right:4px;">code</span> content. Make with ` `` ` render brackets.
- `image`: Image content.
- `graphic`: Vector graphic content.
- `group`: Group of several snips (or more groups).


