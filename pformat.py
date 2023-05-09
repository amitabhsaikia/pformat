# Usage:
#   print(F().c121.b.S('Testing').e.n)

import os


class C:
  """Standard terminal foreground colors"""
  BLACK   = 30
  WHITE   = 37
  RED     = 31
  GREEN   = 32
  YELLOW  = 33
  BLUE    = 34
  MAGENTA = 35
  CYAN    = 36


class B:
  """Standard terminal background colors"""
  BLACK   = 40
  WHITE   = 47
  RED     = 41
  GREEN   = 42
  YELLOW  = 43
  BLUE    = 44
  MAGENTA = 45
  CYAN    = 46


class F:
  """Formats string on screen, with following functionality using ANSI escape codes.

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
  """
  
  FG = C
  BG = B
  LC = {'[': ']', '(': ')', '{': '}', '<': '>'}


  def __init__(self, base=''):
    self._buf = base

  def __call__(self, suffix=''):
    return self._buf + suffix

  def __str__(self):
    return self._buf

  def __repr__(self):
    return self._buf

  def __getattr__(self, attr):
    try:
      attr = attr.lower()
      if attr in ['clr', 'cls', 'clear']:
        self._buf += '\033[1J'
      elif attr in ['cll', 'cline', 'clearline']:
        self._buf += '\033[2K'
      elif attr in ['rw', 'revert']:
        self._buf += '\033[2F'
      elif attr in ['b', 'bold', 'bright']:
        self._buf += '\033[1m'
      elif attr in ['d', 'dim', 'dull']:
        self._buf += '\033[2m'
      elif attr in ['u', 'underline']:
        self._buf += '\033[4m'
      elif attr in ['m', 'magic']:
        self._buf += '\033[5m'
      elif attr in ['t', 'tabs']:
        self._buf += '\t'
      elif attr in ['n', 'newline']:
        self._buf += '\n'
      elif attr.startswith('c'):
        self._buf += f'\033[38;5;{int(attr[1:])}m'
      elif attr.startswith('b'):
        self._buf += f'\033[48;5;{int(attr[1:])}m'
      elif attr.startswith('e'):
        self._buf += '\033[m'
      else:
        pass
    finally:
      return self

  def POS(self, n=0, m=0):
    self._buf += f'\033[{n};{m}H'
    return self

  def S(self, s, n=0):
    if n < 0:
      self._buf += f'{s:>{abs(n)}}'
    else:
      self._buf += f'{s:<{n}}'
    return self

  def T(self, n=1):
    self._buf += '\t' * n
    return self

  def N(self, n=1):
    self._buf += '\n' * n
    return self

  def L(self, label, c='[', fg=C.WHITE, bg=B.BLACK):
    self._buf += f'{c}\033[1;{fg}m\033[1;{bg}m{label}\033[m{F.LC[c]}'
    return self

  def HR(self, n=1, c='-'):
    self._buf += F.DrawHLine(n, c)
    return self

  @classmethod
  def DrawHLine(cls, n=1, c='-'):
    l = cls.COLS
    if n <= 5:
      l = int(l / max(n, 1))
    else:
      l = n
    return c * l

  @staticmethod
  def COLS():
    try:
      return os.get_terminal_size().columns
    except:
      return 80

  @staticmethod
  def ROWS():
    try:
      return os.get_terminal_size().rows
    except:
      return 30

