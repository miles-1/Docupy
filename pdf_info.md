# Terms

- **catalog**: the primary dictionary object containing references directly or indirectly to all other objects in the document with the exception that there may be objects in the trailer that are not referred to by the catalog

- **character**: numeric code representing an abstract symbol according to some defined character encoding rule. There are three manifestations of characters in PDF, depending on context:
    1. A PDF file is represented as a sequence of 8-bit bytes, some of which are interpreted as character codes in the ASCII character set and some of which are treated as arbitrary binary data depending upon the context.
    2. The contents (data) of a string or stream object in some contexts are interpreted as character codes in the PDFDocEncoding or UTF-16 character set.
    3. The contents of a string within a PDF content stream in some situations are interpreted as character codes that select glyphs to be drawn on the page according to a character encoding that is associated with the text font.

- **character set**: a defined set of symbols each assigned a unique character value

- **content stream**: stream object whose data consists of a sequence of instructions describing the graphical elements to be painted on a page

- **cross reference table**: data structure that contains the byte offset start for each of the indirect objects within the file

- **dictionary object**: an associative table containing pairs of objects, the first object being a name object serving as the key and the second object serving as the value and may be any kind of object including another dictionary

- **direct object**: any object that has not been made into an indirect object

- **electronic document**: electronic representation of a page-oriented aggregation of text, image and graphic data, and metadata useful to identify, understand and render that data, that can be reproduced on paper or displayed without significant loss of its information content

- **end-of-line marker (EOL marker)**: one or two character sequence marking the end of a line of text, consisting of a CARRIAGE RETURN character (0Dh) or a LINE FEED character (0Ah) or a CARRIAGE RETURN followed immediately by a LINE FEED

- **FDF file**: File conforming to the Forms Data Format containing form data or annotations that may be imported into a PDF
file (see 12.7.7, “Forms Data Format”)

- **filter**: an optional part of the specification of a stream object, indicating how the data in the stream should be decoded before it is used

- **font**: identified collection of graphics that may be glyphs or other graphic elements

- **function**: a special type of object that represents parameterized classes, including mathematical formulas and sampled representations with arbitrary resolution

- **glyph**: recognizable abstract graphic symbol that is independent of any specific design

- **graphic state**: the top of a push down stack of the graphics control parameters that define the current global framework within which the graphics operators execute

- **ICC profile**: colour profile conforming to the ICC specification [ISO 15076-1:2005]

- **indirect object**: an object that is labeled with a positive integer object number followed by a non-negative integer generation number followed by obj and having endobj after it

- **integer object**: mathematical integers with an implementation specified interval centered at 0 and written as one or more decimal digits optionally preceded by a sign

- **name object**: an atomic symbol uniquely defined by a sequence of characters introduced by a SOLIDUS (/), (2Fh) but the SOLIDUS is not considered to be part of the name

- **name tree**: similar to a dictionary that associates keys and values but the keys in a name tree are strings and are ordered

- **null object**: a single object of type null, denoted by the keyword null, and having a type and value that are unequal to those of any other object

- **number tree**: similar to a dictionary that associates keys and values but the keys in a number tree are integers and are ordered

- **numeric object**: either an integer object or a real object

- **object**: a basic data structure from which PDF files are constructed and includes these types: array, Boolean, dictionary, integer, name, null, real, stream and string

- **object reference**: an object value used to allow one object to refer to another; that has the form “<n> <m> R” where <n> is an indirect object number, <m> is its version number and R is the uppercase letter R

- **object stream**: a stream that contains a sequence of PDF objects

- **real object**: approximate mathematical real numbers, but with limited range and precision and written as one or more decimal digits with an optional sign and a leading, trailing, or embedded PERIOD (2Eh) (decimal point)

- **rectangle**: a specific array object used to describe locations on a page and bounding boxes for a variety of objects and written as an array of four numbers giving the coordinates of a pair of diagonally opposite corners, typically in the form [ llx lly urx ury ] specifying the lower-left x, lower-left y, upper-right x, and upper-right y coordinates of the rectangle, in that order

- **resource dictionary**: associates resource names, used in content streams, with the resource objects themselves and organized into
various categories (e.g., Font, ColorSpace, Pattern)

- **space character**: text string character used to represent orthographic white space in text strings. Space characters include:
    - HORIZONTAL TAB (U+0009)
    - LINE FEED (U+000A)
    - VERTICAL TAB (U+000B)
    - FORM FEED (U+000C)
    - CARRIAGE RETURN (U+000D)
    - SPACE (U+0020)
    - NOBREAK SPACE (U+00A0)
    - EN SPACE (U+2002)
    - EM SPACE (U+2003)
    - FIGURE SPACE (U+2007)
    - PUNCTUATION SPACE (U+2008)
    - THIN SPACE (U+2009)
    - HAIR SPACE (U+200A)
    - ZERO WIDTH SPACE (U+200B)
    - IDEOGRAPHIC SPACE (U+3000)

- **stream object**: consists of a dictionary followed by zero or more bytes bracketed between the keywords stream and endstream

- **string object**: consists of a series of bytes (unsigned integer values in the range 0 to 255) and the bytes are not integer objects, but are stored in a more compact form

- **web capture**: refers to the process of creating PDF content by importing and possibly converting internet-based or locally-resident files. The files being imported may be any arbitrary format, such as HTML, GIF, JPEG, text, and PDF

- **white-space character**: characters that separate PDF syntactic constructs such as names and numbers from each other (see Table 1 in 7.2.2, “Character Set”). white space characters are:
    - HORIZONTAL TAB (09h)
    - LINE FEED (0Ah)
    - FORM FEED (0Ch)
    - CARRIAGE RETURN (0Dh)
    - SPACE (20h)

- **XFDF file:** file conforming to the XML Forms Data Format 2.0 specification, which is an XML transliteration of Forms Data Format (FDF)

- **XMP packet**: structured wrapper for serialized XML metadata that can be embedded in a wide variety of file formats

# Syntax


