import textwrap
from curtsies import Input, FSArray , CursorAwareWindow, fsarray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow
import curtsies


def keys(true, false, default):
    true = default and true.upper() or true.lower()
    false = (not default) and false.upper() or false.lower()
    return ' [{}/{}]'.format(true, false)

def confirm(prompt, true='yes', false='no', *, default=False, single_key=False, true_key='y', false_key='n'):
    with CursorAwareWindow(extra_bytes_callback=lambda x: x) as window:
        prompt = prompt + keys(true_key, false_key, default)
        width = min(min(window.width, 80) - len(true+false) - 5, len(prompt))
        prompt_arr = fsarray((bold(line) for line in textwrap.wrap(prompt, width=width)), width=window.width)
        choice = fsarray(['  '.join((true, false))])
        # prompt_arr[0:1, width+1:width+len(true+false)+5] = choice
        window.render_to_terminal(prompt_arr)
        selected = None
        with Input() as keyGen:
            for i in keyGen:
                if i == true_key:
                    if single_key:
                        return True
                    selected = True
                elif i == false_key:
                    if single_key:
                        return False
                    selected = False
                elif i in ('<LEFT>', '<UP>', '<DOWN>', '<RIGHT>'):
                    selected = not selected
                elif i == '<Ctrl-j>':
                    if selected is not None:
                        return selected
                    return default
                if (selected is not None):
                    choice = fsarray([true if selected else false])
                    prompt_arr[0:1, width+1:width+len(true+false)+5] = choice
                    window.render_to_terminal(prompt_arr)


