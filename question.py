#!/usr/bin/env python
# -*- coding: utf-8 -*-

from answers import prompts

if __name__ == "__main__":
    c = prompts.choice('Choose an option\nwith detail on second line', ['option 1', 'option 2', 'option 2'])
    c = prompts.choice('Choose a thing', ['thing 1\npart 1', 'thing 1\npart2 2', 'thing 2', 'thing 3'])
    c = prompts.choice('Finally choose some letters', ['abcd', 'efgh', 'ijkl', 'mnop'])
