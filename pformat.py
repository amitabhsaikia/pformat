import os
import re


class Color:
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
# Add as property
for k, v in Color.COLOR_MAP.items():
  setattr(Color, k, v[0])
  for i in range(1, len(v)):
    setattr(Color, f'{k}{i}', v[i])


class AL:
  """Standard alignment"""
  LEFT = 0
  CENTER = 1
  RIGHT = 2


class F:
  WIDTH = 24
  CHAR_MAP = {
    'cls': '\033[1J', 'cll': '\033[2K', 'u': '\033[4m', 'm': '\033[5m',
    'ws':  ' ', 'ts':  '\t', 'n':   '\n', '(': ')', '[': ']', '{': '}', '<': '>'
  }

  def __init__(self, base=''):
    self._buffer = base
    self._pb = None
    self._iter = 0.0

  # --------------------------------------------------------------------------------
  # Progress Bar
  # --------------------------------------------------------------------------------
  def StartProgressBar(self, title, total=100, bar_width=100, color=Color.WHITE):
    self._pb = [title, total, bar_width, color]
    return self

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

  def L(self, label, c='[', fg=Color.WHITE, bg=Color.BLACK):
    self._buffer += f'{c}\033[38;5;{fg}m\033[48;5;{bg}m{label.upper()}\033[m{F.CHAR_MAP[c]}'
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
      if attr.upper() in Color.COLOR_MAP:
        return Color.COLOR_MAP[attr.upper()][0]

      attr = attr.lower()
      if attr == 'e':
        self._buffer += '\033[0m'
      elif attr in F.CHAR_MAP:
        self._buffer += F.CHAR_MAP[attr]

      elif attr.startswith('sb'):
        step = (int(attr[2:]) or 1) + 1
        self._buffer += f'\033[{step}F'

      elif attr.startswith('sf'):
        step = (int(attr[2:]) or 1)
        self._buffer += f'\033[{step}E'

      # All color mappings.
      elif attr.startswith('fg_'):
        parts = re.split('(\d+)', attr[3:])
        color = parts[0].upper()
        num = int(parts[1]) if len(parts) > 1 else 0
        if color in Color.COLOR_MAP:
          num = 0 if num > len(Color.COLOR_MAP[color]) else Color.COLOR_MAP[color][num]
        if self._pb:
          self._pb[3] = num
        else:
          self._buffer += f'\033[38;5;{num}m'

      elif attr.startswith('bg_'):
        parts = re.split('(\d+)', attr[3:])
        color = parts[0].upper()
        num = int(parts[1]) if len(parts) > 1 else 0
        if color in Color.COLOR_MAP:
          num = 0 if num > len(Color.COLOR_MAP[color]) else Color.COLOR_MAP[color][num]
        if self._pb:
          self._pb[3] = num
        else:
          self._buffer += f'\033[48;5;{num}m'

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
    print('-' * 80)
    w = 16
    
    s = ''
    a = ''
    for i in range(16):
      s += f'\033[48;5;{i}m{i:>4}\033[m'
      a += f'\033[48;5;{i}m{" ":>4}\033[m'
    print(a)
    print(s)
    
    for i in range(6):
      s = ''
      a = ''
      for j in range(36):
        num = i * 35 + j + 16 + i
        s += f'\033[48;5;{num}m{num:>4}\033[m'
        a += f'\033[48;5;{num}m{" ":>4}\033[m'
      print(a)
      print(s)
        
    s = ''
    a = ''
    for i in range(232, 256):
      s += f'\033[48;5;{i}m\033[38;5;{232 + (256 - i + 1)}m{i:^4}\033[m'
      a += f'\033[48;5;{i}m{" ":>4}\033[m'
    print(a)
    print(s)
    print('-' * 80)

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

    pb = F().StartProgressBar( 'Download', 57, 40)
    i = 0
    while pb.UpdateProgress(1, files[i%len(files)]):
      time.sleep(0.01)
      i += 1

  @staticmethod
  def testF():
    print(F().cls)
    print(F().POS(4, 60).S('Text at 4, 16'))
    print('Testing title bar...\n')
    print(F.draw_title('Title', 2, '='))
    print(F.draw_title('Title', 2, '#'))
    print(F.draw_title('Title', 2, '_', AL.RIGHT))
    print('Testing lines...\n')
    print(F().H1.NL.H2.NL.H3.NL.H4.NL.H5.NL.H80.NL)
    print('Testing formatting and coloring...\n')
    print(F()
      .NL.TS.FG_130.S('new line and tab').E
      .NL.TS.BG_130.S('new line and tab').E
      .NL.TS.S('new line and tab').E
      .NL2.TS2.S('2 line and 2 tab').E
      .NL.L('INFO').WS.S('Logging')
      .NL.L('WARNING', fg=Color.ORANGE).WS.S('Logging')
      .NL.P('key', 'value')
      .NL.A('key', 'value')
      .NL.S('first').WS10.S('name')
      .NL.FG_RED.BG_YELLOW.S('string with foreground and background').E
      .NL.FG_161.S('FG 161').E
      .NL.BG_121.S('BG 121').E)
    print(F().SF4.S('Step forward 4 lines'))
    print(F().SB2.S('Step back 2 lines (written after "Step forward 4 lines")'))
    print(F().SF2.S('Now back to normal'))

