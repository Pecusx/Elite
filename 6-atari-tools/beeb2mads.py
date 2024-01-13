import re
import sys

replacements = {
    r'P%': r'*',  # P% to * -- P% A special symbol which returns the current address being assembled
    r'^\\': ';',  # Replace \ with ; (at the beginning of the line)
    r'\\ ': '; ',  # later in line.
    r'\\$': ';',  # Replace \ with ; (at the end of the line)
    r'^\.': '',  # remove the dot from label definitions (MIGHT BREAK OTHER STUFF)
    r'([A-Za-z]+)%': r'\1__',  # var ending % replaced with __ (not used in original source)
    r'&([0-9A-Fa-f]+)': r'$\1',  # &BACA to $BACA
    r'SKIP (\d+)': r' .ds \1',  # SKIP 4 to .ds 4
    r'EQUB ': ' .by ',  # bytes
    r'CHAR ': ' .by ',  # chars
    r'EQUW ': ' .wo ',  # words
    # r'(?<=PRINT.*)(\~)': ''  # removes ~ from PRINT statements (~ means display in HEX)
    # the above regex does not work in python re lib (no lookbehind for variable length pattern)
    r'PRINT(.*)\~(.*)': r'PRINT\1\2',  # remove 1 tilde from a line w/ PRINT
    r'PRIN(.*)\~(.*)': r'PRIN\1\2',  # remove the second tilde (haxxx)
    r'PRINT': ' .PRINT',
    r'INCLUDE ': r' ICL ',
    # r'(?<=[\w)])\s*AND\s*(?=[\w(])': ' & ',  # bitwise operators (not werking)
    # r'(?<!^)(?<![ \t\w;:])\bOR\b': '|',
    # r'(?<!^)(?<![ \t\w;:])\bXOR\b': '^',
    # r'(?<!^)(?<![ \t\w;:])\bNOT\b': '~',

}


def apply_replacements(text, replacements):
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    # ------------additional transformations------------
    # multiline comment
    #text = re.sub(r'(\*{10,}.*?\*{10,})', r'/\1/', text, flags=re.DOTALL)

    # add beeb macros
    macros = ('; -----MADS BEEB replacement macros-----\n'
              '     .MACRO GUARD addr\n'
              '        .IF * > :addr\n'
              '            .ERROR :addr, " GUARD ERROR: ", *\n'
              '        .ENDIF\n'
              '     .ENDM\n'
              '; -----end of MADS replacement macros-----\n'
              '\n')
    text = macros + text
    return text


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        src = f.read()
    out = apply_replacements(src, replacements)
    print(out)
