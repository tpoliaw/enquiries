__author__ = 'Peter Holloway'
from answers.yesno import confirm
from answers.choices import choose
from answers.document import prompt as freetext

__all__ = ['confirm', 'choose', 'freetext']

del yesno, choices, document
