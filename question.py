#!/usr/bin/env python
# -*- coding: utf-8 -*-

from answers import prompts
from answers import yesno

if __name__ == "__main__":
    c = prompts.choice('Choose an option', ['option 1', 'option 2', 'option 3'])
    print('Option: {}'.format(c))
    c = prompts.choice('Choose a thing', ['thing 1 part 1', 'thing 1\npart 2', 'thing 2', 'thing 3'])
    print('Thing {}'.format(c))
    c = prompts.choice('Pick a number', [1234, 4238, 43230, 209348], multi=False)
    print('Number: {}'.format(c))
    c = prompts.choice('Finally choose some letters', ['abcd', 'efgh', 'ijkl', 'mnop'])
    print('Letters: {}'.format(', '.join(c)))
    res = yesno.confirm('Are you sure?')
    print('Very sure' if res else 'Not sure')
    res = yesno.confirm('Do you want to continue?', 'Indeed', 'Of course not', single_key=True, default=True)
    print('Continuing' if res else 'Aborting')
