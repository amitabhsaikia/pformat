# pformat
Format strings with ease with ANSI codes and use TPUT easily in python

# Testing:
```
   python3 -c 'import pformat; pformat.F.color_palatte()'
   python3 -c 'import pformat; pformat.F.testF()'
   python3 -c 'import pformat; pformat.F.testPB()'
```
  
# Usage:
```
  print(F().c121.b.S('Testing').e.n)
```

# Documentation:
Formats string on screen, with following functionality using ANSI escape codes.

At class level:

    * draw_line                   - Draw horizontal line with default character '-'
    * draw_title                  - Draw a title and lines around

At instance level:

    * L(label, c='char', fg, bg)  - Create a label 'test' and format it as '[test]'
    * P(key, value, num, sep)     - Formats as 'key    : value'
    * A(key, value, num, sep)     - Formats as '   key - value'
    * S(s, n)       - 's' string with 'n' indentation. Negative numbers indents to right.
    * POS(n, m)     - Position the string at n-th row and m-th column.

Quirky level:

    * e           - End quirky mode
    * cls         - Clear the screen
    * cll         - Clear the line
    * sb          - Step Back n lines
    * u           - Underline the subsequent string
    * m           - Blink the subsequent string
    * h[N]        - Draw horizontal line of length N
    * nl[N]       - Add a newline or do it N times
    * ts[N]       - Add a tab or do it N times
    * ws[N]       - Add a tab or do it N times
    * fg_[0-255]  - Change the foreground of the subsequent string
    * bg_[0-255]  - Change the background of the subsequent string
    * fg_[NAME[INDEX]]  - Change the foreground with named color
    * bg_[NAME[INDEX]]  - Change the background with named color

Color Names:

    BLACK, WHITE, GRAY, RED, BLUE, GREEN, YELLOW
    ORANGE, BROWN, PURPLE, VIOLET, AQUA, TEAL, OLIVE, PINK


