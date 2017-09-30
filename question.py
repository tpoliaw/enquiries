#!/usr/bin/env python
# -*- coding: utf-8 -*-

from answers import prompts

if __name__ == "__main__":
    for i in range(3):
        c = prompts.choice('Prompt {}: '.format(i), ['abcd', 'efgh', 'ijkl', 'mnop'])
