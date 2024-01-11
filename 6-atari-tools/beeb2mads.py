import re
import sys

replacements = {
    r'^\\': ';',  # Replace \ with ; (at the beginning of the line)
    r'\\ ': '; ',  # later in line.
    r'\\$': ';',   # Replace \ with ; (at the end of the line)
    r'&([0-9A-Fa-f]+)': r'$\1',  # &BACA to $BACA
    r'SKIP (\d+)': r' .ds \1',  # SKIP 4 to .ds 4
    r'P%': r'*',  # P% to * -- P% A special symbol which returns the current address being assembled
    # r'(?<=PRINT.*)(\~)': ''  # removes ~ from PRINT statements (~ means display in HEX)
    # the above regex does not work in python re lib (no lookbehind for variable length pattern)
    r'PRINT(.*)\~(.*)': r'PRINT\1\2',  # remove 1 tilde from a line w/ PRINT
    r'PRIN(.*)\~(.*)': r'PRIN\1\2',  # remove the second tilde (haxxx)

}


def apply_replacements(text, replacements):
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        src = f.read()
    out = apply_replacements(src, replacements)
    print(out)
