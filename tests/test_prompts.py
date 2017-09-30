import pytest
from answers import prompts

@pytest.fixture
def clist():
    import answers
    cl = answers.prompts.ChoiceList(['abcd', 'efgh', 'ijkl'])
    return cl

def test_list_length(clist):
    assert len(clist) == 3

def test_get_item(clist):
    assert clist[1] == prompts.UNCHECKED + "efgh"

def test_contains(clist):
    assert 'efgh' in clist
    assert 'refwe' not in clist

def test_set_item(clist):
    assert clist[1] == prompts.UNCHECKED + 'efgh'
    clist[1] = 'mnop'
    assert clist[1] == prompts.UNCHECKED + 'mnop'

def test_del_item(clist):
    del clist[1]
    assert clist[1] != prompts.UNCHECKED + 'abcd'

def test_iterate(clist):
    choices = iter(clist)
    assert next(choices) == prompts.UNCHECKED + 'abcd'
    assert next(choices) == prompts.UNCHECKED + 'efgh'
    assert next(choices) == prompts.UNCHECKED + 'ijkl'
    with pytest.raises(StopIteration, message='Iterator should have stopped'):
        next(choices)

def test_reverse(clist):
    choices = reversed(clist)
    assert next(choices) == prompts.UNCHECKED + 'ijkl'

def test_no_choices():
    with pytest.raises(ValueError):
        prompts.ChoiceList([])

def test_check_option(clist):
    clist.check()
    assert clist[0] == prompts.CHECKED + 'abcd'
    clist.check()
    assert clist[0] == prompts.UNCHECKED + 'abcd'

    clist.select(1)
    assert clist[1] == prompts.UNCHECKED + 'efgh'
    clist.check()
    assert clist[1] == prompts.CHECKED + 'efgh'


