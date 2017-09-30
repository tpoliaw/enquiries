from curtsies import FullscreenWindow, Input, FSArray , CursorAwareWindow
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow

import random

CHECKED = '\U0001f78a '
UNCHECKED = '\U0001f785 '

def choice(prompt, choices):
    plines = prompt.split('\n')
    plen = len(plines)
    choice_list = ChoiceList(choices)
    index = 0
    with CursorAwareWindow(extra_bytes_callback=lambda x: x) as window:
        with Input() as inGen:
            parr = FSArray(plen, window.width)
            for i, line in enumerate(plines):
                parr[i:i+1, 0:len(line)] = [line]
            arr = choice_list.render(window.width)
            arr.rows = parr.rows + arr.rows
            window.render_to_terminal(arr)
            for i in inGen:
                if i == '<DOWN>':
                    index = min(len(choices)-1, index+1)
                    choice_list.select(index)
                elif i == '<UP>':
                    index = max(0, index-1)
                    choice_list.select(index)
                elif i == '<SPACE>':
                    choice_list.check()
                    option = choice_list[index]
                    break
                arr = choice_list.render(window.width)
                arr.rows = parr.rows + arr.rows
                window.render_to_terminal(arr)

    print('{}: {}'.format(prompt, option))
    return option

class Choice:
    def __init__(self, obj):
        self._obj = obj
        self._selected = False

    def check(self):
        self._selected = not self._selected

    def __str__(self):
        state = CHECKED if self._selected else UNCHECKED
        s = '{}{}'.format(state, self._obj)
        return '\n  '.join(s.split('\n'))


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
        arr = FSArray(len(self._choices), width)
        l = 0
        for i, option in enumerate(self._choices):
            lines = str(option).split('\n')
            if i == self._idx:
                fmt = bold
            else:
                fmt = self._fmt
            for j, line in enumerate(lines, l):
                arr[j:j+1, 0:len(line)] = [fmt(line)]
                l += 1
        return arr

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
