from curtsies import Input, FSArray, CursorAwareWindow, fsarray
from curtsies.events import PasteEvent
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow
import textwrap
import itertools
from collections import namedtuple
import enum
import re


WORD_BREAK = re.compile('[^\w]')

Cursor = namedtuple('Cursor', ['row', 'column'])


class Dir(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Document:
    def __init__(self, text='', cursor=None):
        if cursor is None:
            cursor = len(text)
        self._lbuffer = text[:cursor]
        self._rbuffer = text[cursor:]

    def handle(self, key):
        if len(key) == 1:
            self.add(key)
        elif key == '<SPACE>':
            self.add(' ')
        elif key == '<BACKSPACE>':
            self.bksp()
        elif key == '<DELETE>':
            self.bksp(Dir.RIGHT)
        elif key == '<Ctrl-j>':
            self.add('\n')

    def add(self, key):
        self._lbuffer += key

    def bksp(self, direction=Dir.LEFT):
        if direction == Dir.LEFT:
            self._lbuffer = self._lbuffer[:-1]
        elif direction == Dir.RIGHT:
            self._rbuffer = self._rbuffer[1:]

    def move_cursor(self, direction=Dir.LEFT):
        if direction == Dir.LEFT:
            if self._lbuffer:
                c = self._lbuffer[-1]
                self._lbuffer = self._lbuffer[:-1]
                self._rbuffer = c + self._rbuffer
        elif direction == Dir.RIGHT:
            if self._rbuffer:
                c = self._rbuffer[0]
                self._lbuffer += c
                self._rbuffer = self._rbuffer[1:]
        elif direction == Dir.UP:
            split = self._lbuffer.rsplit('\n', 2)
            if len(split) == 1:
                return
            left = '\n'.join((*split[:-2], split[-2][:len(split[-1])]))
            old_len = len(self._lbuffer)
            new_len = len(left)
            self._lbuffer, self._rbuffer = self._lbuffer[:new_len], self._lbuffer[new_len:] + self._rbuffer
        elif direction == Dir.DOWN:
            rs = self._rbuffer.split('\n', 2)
            if len(rs) == 1:
                return
            ls = self._lbuffer.rsplit('\n', 1)
            indent = len(ls[-1])
            self._lbuffer, self._rbuffer = (
                    self._lbuffer + rs[0] + '\n' + rs[1][:indent],
                    '\n'.join((rs[1][indent:], *rs[2:]))
            )

    def move_word(self, direction=Dir.LEFT, delete=False):
        if direction == Dir.LEFT:
            words = WORD_BREAK.split(self._lbuffer)
            spaces = 0
            while spaces < len(words)-1 and words[-1-spaces] == '':
                spaces += 1
            last_word = words[-1-spaces]
            self._lbuffer, self._rbuffer = (
                    self._lbuffer[:-len(last_word)-spaces],
                    (self._lbuffer[-len(last_word)-spaces:] + self._rbuffer) if not delete else self._rbuffer
            )
        elif direction == Dir.RIGHT:
            words = WORD_BREAK.split(self._rbuffer)
            spaces = 0
            while spaces < len(words)-1 and words[spaces] == '':
                spaces += 1
            first_word = words[spaces]
            self._lbuffer, self._rbuffer = (
                    (self._lbuffer + self._rbuffer[:len(first_word)+spaces]) if not delete else self._lbuffer,
                    self._rbuffer[spaces+len(first_word):]
            )

    @property
    def lines(self):
        return str(self).split('\n')

    @property
    def cursor(self):
        lines = self._lbuffer.split('\n')
        return Cursor(len(lines)-1, len(lines[-1]))

    def __str__(self):
        return self._lbuffer+self._rbuffer

def prompt(msg):
    with CursorAwareWindow(extra_bytes_callback=lambda x:x, hide_cursor=False) as window:
        prompt = textwrap.wrap(msg+'\n', window.width)
        p_lines = len(prompt)
        document = Document()
        window.render_to_terminal(fsarray(prompt+['']), (1,0))
        with Input() as keys:
            for key in keys:
                if key == '<Ctrl-j>': # return
                    window.render_to_terminal([], (0,0))
                    return str(document)
                if key == '<Esc+Ctrl-J>': # alt-return
                    document.handle('<Ctrl-j>')
                elif key == '<LEFT>':
                    document.move_cursor(Dir.LEFT)
                elif key == '<RIGHT>':
                    document.move_cursor(Dir.RIGHT)
                elif key == '<UP>':
                    document.move_cursor(Dir.UP)
                elif key == '<DOWN>':
                    document.move_cursor(Dir.DOWN)
                elif key == '<Ctrl-LEFT>':
                    document.move_word(Dir.LEFT)
                elif key == '<Ctrl-RIGHT>':
                    document.move_word(Dir.RIGHT)
                elif key == '<Ctrl-w>':
                    document.move_word(Dir.LEFT, delete=True)
                elif key == '<Ctrl-DELETE>':
                    document.move_word(Dir.RIGHT, delete=True)
                elif isinstance(key, PasteEvent):
                    for c in key.events:
                        document.handle(c)
                else:
                    document.handle(key)
                text = prompt + document.lines
                r, c = document.cursor
                lines, cursor = _wrap(text, Cursor(r+p_lines, c), window.width)
                window.render_to_terminal(fsarray(lines), cursor)

def _wrap(text, cursor, width):
    """Convert an iterable of lines to an iterable of wrapped lines"""
    text = [textwrap.wrap(line, width, drop_whitespace=False) or [''] for line in text]
    # logger.debug('wrapped lines: %s', text)
    previous_lines = sum(len(line) for line in text[:cursor.row])
    current_line = text[cursor.row]
    row, column = _current_word(current_line, cursor.column)
    row += previous_lines
    return itertools.chain(*text), Cursor(row, column)

def _current_word(words, column):
    if column == 0: return 0,0
    count = 0
    for i, w in enumerate(words):
        end = count + len(w)
        if column <= end:
            return (i, column-count)
        count += len(w)
    else:
        raise ValueError('column %d is not in words (%s)' %(column, words))
