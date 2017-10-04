import pytest

@pytest.fixture
def doc():
    import answers
    return answers.Document()

@pytest.fixture
def full_doc():
    import answers
    return answers.Document('this is a paragraph\nof text')


def test_add_keys(doc):
    doc.add('a')
    assert str(doc) == 'a'
    doc.add('b')
    assert str(doc) == 'ab'

def test_home(full_doc):
    pass

def test_bksp(full_doc):
    full_doc.bksp()
    assert str(full_doc) == 'this is a paragraph\nof tex'
    full_doc.bksp()
    assert str(full_doc) == 'this is a paragraph\nof te'

