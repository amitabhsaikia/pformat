# Usage:
#   print(F().c121.b.S('Testing').e.n)

import os


class FG:
  """Standard terminal foreground colors"""
  BLACK   = 30
  WHITE   = 37
  RED     = 31
  GREEN   = 32
  YELLOW  = 33
  BLUE    = 34
  MAGENTA = 35
  CYAN    = 36

class BG:
  """Standard terminal background colors"""
  BLACK   = 40
  WHITE   = 47
  RED     = 41
  GREEN   = 42
  YELLOW  = 43
  BLUE    = 44
  MAGENTA = 45
  CYAN    = 46

class AL:
  """Standard alignment"""
  LEFT = 0
  CENTER = 1
  RIGHT = 2

class F:
  """Formats string on screen, with following functionality using ANSI escape codes.

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
    * clr|CLR|cls|CLS|clear|CLEAR               - Clear the screen
    * cll|CLL|clearline|CLEARLINE|cline|CLINE   - Clear the line
    * rw|RW|revert|REVERT                       - Go back to the previous line
    * b|B|bold|BOLD|bright|BRIGHT               - Bolden the subsequent string
    * d|D|dim|DIM|dull|DULL                     - Lighten the subsequent string
    * u|U|underline|UNDERLINE                   - Underline the subsequent string
    * m|M|magic|MAGIC                           - Blink the subsequent string
    * e                                         - End quirky mode
    * h[N]                                      - Draw horizontal line of length N
    * n[N]                                      - Add a newline or do it N times
    * t[N]                                      - Add a tab or do it N times
    * c[0-255]                                  - Change the foreground of the subsequent string
    * b[0-255]                                  - Change the background of the subsequent string
  """
  
  WIDTH = 24
  CHARSET = ['\033[1J', '\033[2K', '\033[2F', '\033[1m',
             '\033[2m', '\033[4m', '\033[5m', '\033[m',
             ' ', '\t', '\n', ']', ')', '}', '>']
  CMAP = {'cls':0, 'clr':0, 'clear':0,
          'cll':1, 'cline':1, 'clearline':1,
          'rw':2, 'revert':2, 'roll':2,
          'b':3, 'bold':3, 'bright':3, 'd':4, 'dim':4, 'dull':4,
          'u':5, 'underline':5, 'm':6, 'magic':6, 'blink':6, 'e': 7,
          'ws':8, 'tab':9, 'tabs':9, 'n':10, 'newline':10,
          '[':11, '(':12, '{':13, '<':14}


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
      if attr in F.CMAP:
        self._buf += F.CHARSET[F.CMAP[attr]]
      elif attr.startswith('t'):                            # Add N tabs e.g. 't2' will add 2 tabs
        self._buf += '\t' * int(attr[1:] or 1)
      elif attr.startswith('n'):                            # Add N newlines e.g. 'n3' will add 3 new lines
        self._buf += '\n' * int(attr[1:] or 1)
      elif attr.startswith('w'):                            # Add N whitespaces e.g. 'w2' will add 2 tabs
        self._buf += ' ' * int(attr[1:] or 1)
      elif attr.startswith('h'):                            # Add horizontal of the given lenght ratio
        self._buf += F.draw_line(int(attr[1:] or 1))
      elif attr.startswith('c'):                            # Add color e.g. c120 will color red.
        self._buf += f'\033[38;5;{int(attr[1:])}m'
      elif attr.startswith('b'):                            # Add background color e.g. b200
        self._buf += f'\033[48;5;{int(attr[1:])}m'
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

  def L(self, label, c='[', fg=FG.WHITE, bg=BG.BLACK):
    self._buf += f'{c}\033[1;{fg}m\033[1;{bg}m{label}\033[m{F.CHARSET[F.CMAP[c]]}'
    return self

  def P(self, k, v, num=None, sep=':'):
    if num:
      self._buf += f'{num}. {k:<{F.WIDTH - len(str(num)) - 2}} {sep} {k}'
    else:
      self._buf += f'{k:<{F.WIDTH}} {sep} {k}'
    return self

  def A(self, k, v, num=None, sep='-'):
    if num:
      self._buf += f'{num}. {k:>{F.WIDTH - len(str(num)) - 2}} {sep} {k}'
    else:
      self._buf += f'{k:>{F.WIDTH}} {sep} {k}'
    return self

  @classmethod
  def draw_title(self, title, n=1, c='-', align=AL.LEFT):
    hl = int((F.LWIDTH(n) - len(title) - 2) / 2)
    left = hl
    right = hl
    if align == AL.LEFT:
      left = 3
      right = hl + (hl - 3)
    elif align == AL.RIGHT:
      left = hl + (hl - 3)
      right = 3
    return ' '.join([left * c, title, right * c])
    
  @classmethod
  def draw_line(cls, n=1, c='-'):
    return c * F.LWIDTH(n)

  @staticmethod
  def COLS(default=80):
    try:
      return os.get_terminal_size().columns
    except:
      return default

  @staticmethod
  def ROWS(default=30):
    try:
      return os.get_terminal_size().rows
    except:
      return default

  @staticmethod
  def LWIDTH(size=1):
    if size <= 5:
      return int(F.COLS() / max(size, 1))
    else:
      return size

  @staticmethod
  def color_palatte():
    s = 'Foreground:\n'
    for i in range(255):
      s += f'\033[38;5;{i}m{i:3} | '
      if (i + 1) % 15 == 0:
        s += '\n'
    print(s)
    s = '\nBackground:\n'
    for i in range(255):
      s += f'\033[48;5;{i}m{i:5} |'
      if (i + 1) % 15 == 0:
        s += '\n'
    print(s)

  @staticmethod
  def test():
    print(F.draw_title('Title', 2, '='))
    print(F.draw_title('Title', 2, '^'))
    print(F.draw_title('Title', 2, '#'))
    print(F.draw_title('Title', 2, '_', AL.RIGHT))
    print(F().C254.S('string')
      .n.t.B130.S('new line and tab').e
      .n2.t2.C161.S('2 line and 2 tab').e
      .n.h1.n.h2.n.h3.n.h4.n.h5.n.h6
      .n.P('key', 'value')
      .n.P('key', 'value', 3)
      .n.A('key', 'value')
      .n.A('key', 'value', 5)
      .n.L('INFO').ws.S('Logging')
      .n.S('first').w3.S('name'))
