# Usage:
#   print(F().c121.b.S('Testing').e.n)
#  """Formats string on screen, with following functionality using ANSI escape codes.
#
#  At class level:
#    * draw_line                   - Draw horizontal line with default character '-'
#    * draw_title                  - Draw a title and lines around
#
#  At instance level:
#    * L(label, c='char', fg, bg)  - Create a label 'test' and format it as '[test]'
#    * P(key, value, num, sep)     - Formats as 'key    : value'
#    * A(key, value, num, sep)     - Formats as '   key - value'
#    * S(s, n)       - 's' string with 'n' indentation. Negative numbers indents to right.
#    * POS(n, m)     - Position the string at n-th row and m-th column.
#
#  Quirky level:
#    * clr|CLR|cls|CLS|clear|CLEAR               - Clear the screen
#    * cll|CLL|clearline|CLEARLINE|cline|CLINE   - Clear the line
#    * rw|RW|revert|REVERT                       - Go back to the previous line
#    * b|B|bold|BOLD|bright|BRIGHT               - Bolden the subsequent string
#    * d|D|dim|DIM|dull|DULL                     - Lighten the subsequent string
#    * u|U|underline|UNDERLINE                   - Underline the subsequent string
#    * m|M|magic|MAGIC                           - Blink the subsequent string
#    * e                                         - End quirky mode
#    * h[N]                                      - Draw horizontal line of length N
#    * n[N]                                      - Add a newline or do it N times
#    * t[N]                                      - Add a tab or do it N times
#    * c[0-255]                                  - Change the foreground of the subsequent string
#    * b[0-255]                                  - Change the background of the subsequent string
#  """

import os
import re


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
  
  WIDTH = 24
  CHAR_MAP = {
    'cls': '\033[1J', 'cll': '\033[2K', 'u':   '\033[4m', 'm':   '\033[5m',
    'ws':  ' ', 'ts':  '\t', 'n':   '\n',
    '(': ')', '[': ']', '{': '}', '<': '>'
  }

  COLOR_MAP = {
      'WHITE':  [254, 255],
      'BROWN':  [94, 130, 166, 172],
      'YELLOW': [220, 226, 227, 228, 229],
      'BLACK':  [16, 0, 232, 233, 234, 235],
      'TEAL':   [23, 29, 30, 31, 37, 73, 44, 80, 116],
      'RED':    [52, 88, 124, 125, 160, 161, 196, 197],
      'OLIVE':  [58, 136, 137, 100, 101, 142, 143, 106],
      'ORANGE': [202, 203, 166, 167, 208, 209,214,  215],
      'AQUA':   [45, 81, 117, 51, 87, 123, 159, 195, 45, 81],
      'PINK':   [198, 199, 200, 201, 206, 207, 212, 213, 219, 225],
      'BLUE':   [17, 18, 19, 20, 21, 25, 26, 27, 32, 33, 38, 39, 75],
      'GREEN':  [22, 28, 34, 35, 40, 41, 76, 46, 77, 82, 47, 83, 118, 119],
      'PURPLE': [53, 54, 55, 89, 90, 55, 91, 92, 56, 127, 128, 129, 134, 165],
      'VIOLET': [56, 57, 93, 63, 98, 99, 135, 105, 141, 147],
      'GRAY':   [236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253],
  }

  def __init__(self, base=''):
    self._buffer = base
    self._pb = None
    self._iter = 0.0

  # --------------------------------------------------------------------------------
  # Progress Bar
  # --------------------------------------------------------------------------------
  def StartProgressBar(self, title, total=100, bar_width=100, color=255):
    self._pb = [title, total, bar_width, color]
    pass

  def UpdateProgress(self, count, msg=''):
    self._iter += count
    done = False
    end = ''
    if self._iter >= self._pb[1]:
      self._iter = self._pb[1]
      end = 'Done'
      done = True

    completed = f'{100 * (self._iter / self._pb[1]):0.1f}%'
    iterlen = int(self._pb[2] * self._iter // self._pb[1])
    filled = (f"\033[48;5;{self._pb[3]}m{' ' * iterlen}\033[m" +
              ' ' * (self._pb[2] - iterlen))
    if msg:
      print(f' {self._pb[0]} [{filled}] {completed} {end}')
      print(f'\033[2K > {msg}', end='\r')
      print(f'\033[2F')
    else:
      print(f'{self._pb[0]} [{filled}] {completed} {end}', end='\r')
    if done:
      print('\n')
      self._pb = None
      self._iter = 0.0
      return False
    return True


  def S(self, sobj, indent=0):
    if indent < 0:
      self._buffer += f'{sobj:>{abs(indent)}}'
    else:
      self._buffer += f'{sobj:<{indent}}'
    return self

  def I(self, index, indent=0, sep='.'):
    if indent < 0:
      self._buffer += f'{index + sep:>{abs(indent)}}'
    else:
      self._buffer += f'{index + sep:<{indent}}'
    return self

  def P(self, key, value, sep=':'):
    self._buffer += f'{key:<{F.WIDTH}} {sep} {value}'
    return self

  def A(self, key, value, sep='-'):
    self._buffer += f'{key:>{F.WIDTH}} {sep} {value}'
    return self

  def L(self, label, c='[', fg=FG.WHITE, bg=BG.BLACK):
    self._buffer += f'{c}\033[1;{fg}m\033[1;{bg}m{label}\033[m{F.CHAR_MAP[c]}'
    return self

  def POS(self, row=0, col=0):
    self._buffer += f'\033[{row};{col}H'
    return self

  def __call__(self, suffix=''):
    return self._buffer + suffix

  def __str__(self):
    return self._buffer

  def __repr__(self):
    return self._buffer

  def __getattr__(self, attr):
    try:
      attr = attr.lower()
      if attr == 'e':
        self._buffer += '\033[0m'
      elif attr in F.CHAR_MAP:
        self._buffer += F.CHAR_MAP[attr]

      # All color mappings.
      elif attr.startswith('fg_'):
        parts = re.split('(\d+)', attr[3:])
        color = parts[0].upper()
        num = int(parts[1]) if len(parts) > 1 else 0
        if color in F.COLOR_MAP:
          num = 0 if num > len(F.COLOR_MAP[color]) else F.COLOR_MAP[color][num]
        if self._pb:
          self._pb[3] = num
        else:
          self._buffer += f'\033[38;5;{num}m'

      elif attr.startswith('bg_'):
        parts = re.split('(\d+)', attr[3:])
        color = parts[0].upper()
        num = int(parts[1]) if len(parts) > 1 else 0
        if color in F.COLOR_MAP:
          num = 0 if num > len(F.COLOR_MAP[color]) else F.COLOR_MAP[color][num]
        if self._pb:
          self._pb[3] = num
        else:
          self._buffer += f'\033[34;5;{num}m'

      # Handle whitespaces
      elif attr.startswith('ws'):
        self._buffer += ' ' * int(attr[2:] or 1)
      elif attr.startswith('ts'):
        self._buffer += '\t' * int(attr[2:] or 1)
      elif attr.startswith('nl'):
        self._buffer += '\n' * int(attr[2:] or 1)

      # Handle lines
      elif attr.startswith('h'):
        self._buffer += F.draw_line(int(attr[1:] or 1))

      # Ignore unknowns
      else:
        pass
    finally:
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
      if (i + 1) % 8 == 0:
        s += '\n'
    print(s)

  @staticmethod
  def test():
    print(F.draw_title('Title', 2, '='))
    print(F.draw_title('Title', 2, '#'))
    print(F.draw_title('Title', 2, '_', AL.RIGHT))
    print(F()
      .C254.S('string').nl
      .nl.ts.fg_130.S('new line and tab').e
      .nl.ts.bg_130.S('new line and tab').e
      .nl.ts.bg_.S('new line and tab').e
      .nl2.ts2.fg_161.S('2 line and 2 tab').e
      .nl.h1.nl.h2.nl.h3.nl.h4.nl.h5.nl.h6
      .nl.P('key', 'value')
      .nl.A('key', 'value')
      .nl.L('INFO').ws.S('Logging')
      .nl.S('first').w3.S('name'))

  @staticmethod
  def testPB():
    import time

    files = [
		  'README.md',
		  '../Code/directory_one/verylong.zip',
		  '../Code/file129322.py',
		  '../Code/directory_one/verylong.zip',
		  '../Code/file20.py',
		  '../Code/file1.py',
    ]

    f = F()
    pb = f.StartProgressBar( 'Download', 57, 40)
    i = 0
    while f.UpdateProgress(1, files[i%len(files)]):
      time.sleep(0.01)
      i += 1
    f.DoneProgress()

