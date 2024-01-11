import re
import sys

replacements = {
    r'^\\': ';',  # Replace \ with ; (at the beginning of the line)
    r'\\ ': '; ',  # later in line.
    r'&([0-9A-Fa-f]+)': r'$\1',  # &BACA to $BACA
    r'SKIP (\d+)': r'  .ds \1'  # SKIP 4 to .ds 4
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
