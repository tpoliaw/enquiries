from curtsies import FullscreenWindow, Input, FSArray , CursorAwareWindow
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow

import random

CHECKED = '\U0001f78a '
UNCHECKED = '\U0001f785 '

def choice(prompt, choices):
    plines = prompt.split('\n')
    choice_list = ChoiceList(choices)
    with CursorAwareWindow(extra_bytes_callback=lambda x: x) as window:
        with Input() as inGen:
            parr = FSArray(len(plines), window.width)
            parr.rows = plines
            arr = choice_list.render(window.width)
            arr.rows = parr.rows + arr.rows
            window.render_to_terminal(arr)
            for i in inGen:
                if i == '<DOWN>':
                    choice_list.next()
                elif i == '<UP>':
                    choice_list.prev()
                elif i == '<SPACE>':
                    choice_list.check()
                elif i == '<Ctrl-j>':
                    break
                arr = choice_list.render(window.width)
                arr.rows = parr.rows + arr.rows
                window.render_to_terminal(arr, (0,14))

    options = choice_list.get_selection()
    print('{}: {}'.format(prompt, options))
    return options

class Choice:
    def __init__(self, obj):
        self._obj = obj
        self._selected = False

    def check(self):
        self._selected = not self._selected

    def __str__(self):
        return str(self._obj)
        # state = CHECKED if self._selected else UNCHECKED
        # s = '{}{}'.format(state, self._obj)
        # return '\n  '.join(s.split('\n'))

    def render(self, fmt, width):
        lines = str(self).split('\n')
        arr = FSArray(len(lines), width)
        arr[0:len(lines), 0:width] = [fmt(line) for line in lines]
        return arr


class ChoiceList:
    def __init__(self, choices, fmt=lambda x:x):
        if not choices:
            raise ValueError('No choices given')
        self._choices = [Choice(c) for c in choices]
        self._fmt = fmt
        self._idx = 0

    def check(self):
        state = self._choices[self._idx]
        state.check()

    def select(self, index):
        self._idx = index

    def render(self, width):
        arr = FSArray(0, width)
        for i, option in enumerate(self._choices):
            lines = str(option).split('\n')
            fmt = bold if i == self._idx else self._fmt
            state = CHECKED if option._selected else UNCHECKED
            arr.rows.append(fmt(state + lines[0]))
            rows = [fmt('  ' + line) for line in lines[1:]]
            arr.rows.extend(rows[1:])
        return arr

    def get_selection(self):
        return [item._obj for item in self._choices if item._selected]

    def next(self):
        self._idx = min(len(self)-1, self._idx+1)
    def prev(self):
        self._idx = max(0, self._idx-1)
    def __len__(self):
        return len(self._choices)

    def __getitem__(self, key):
        item = self._choices[key]
        return item._obj

    def __setitem__(self, key, value):
        self._choices[key] = (False, value)

    def __delitem__(self, key):
        del self._choices[key]

    def __contains__(self, item):
        return item in [i[1] for i in self._choices]


if __name__ == "__main__":
    c = choice('Prompt \n line 3: ', ['abc', 'def', 'ghi', 'jkl', 'mno'])
