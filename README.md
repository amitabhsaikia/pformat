# pformat
Format strings with ease with ANSI codes and use TPUT easily in python

Functionality:
  At class level:
    * DrawHLine|HR(c='-')      - Draw horizontal line with default character '-'
    * FG                         - Foreground color
    * BG                         - Background color

  At instance level:
    * L(label, c='char', fg, bg) - Create a label 'test' and format it as '[test]'
    * N(n)          - 'n' new lines
    * T(n)          - 'n' tabs
    * S(s, n)       - 's' string with 'n' indentation. Negative numbers indents to right.
    * POS(n, m)     - Position the string at n-th row and m-th column.

  Quirky level:
    * clr|CLR|cls|CLS|clear|CLEAR               - Clear the screen
    * cll|CLL|clearline|CLEARLINE|cline|CLINE   - Clear the line
    * rw|RW|revert|REVERT                       - Go back to the previous line
    * b|B|bold|BOLD|bright|BRIGHT               - Bolden the subsequent string
    * d|D|dim|DIM|dull|DULL                     - Lighten the subsequent string
    * u|U|underline|UNDERLINE                   - Underline the subsequent string
    * m|M|magic|MAGIC                           - Blink the subsequent string
    * n                                         - Add a single new line
    * t                                         - Add a single tab
    * e                                         - End quirky mode
    * c[0-254]                                  - Change the foreground of the subsequent string
    * b[0-254]                                  - Change the background of the subsequent string


Usage:

print(F().L('my label', c='<', fg=F.FG.RED, bg=F.BG.WHITE).S(' This is a great').n.S('ok').N(3).S('how').n.t.S(' does').T(3).S('it work'))
print(F().CLS.POS(10, 50).C161.S('This is the title'))
print(F().POS(11, 50).B240.HR(30).e.n)
print(F().POS(F.ROWS(), F.COLS()))

