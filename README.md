# Answers

A straightforward way to get decisions from your users.
Offer multiple choice, yes/no, free text, int, float etc.

```
from answers import prompt

options = ['thing 1', 'thing 2', 'thing 3']
choices = prompt.choose('Choose one of these options: ', options, multiple=True)

if prompt.confirm('Do you want to write something?', default=False):
	text = prompt.input('Write something interesting: ')
	print(text)
```
