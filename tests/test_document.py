import answers
import pytest
from unittest import mock

@pytest.fixture
def doc():
    return answers.Document()

sample_text = """this is a piece of sample text containing varying
line
lengths.

And new paragraphs also with multiple lines"""

# @pytest.fixture
# def sample_text():
#     return sample_text

@pytest.fixture
def full_doc():
    return answers.Document(sample_text)

@pytest.fixture
def mock_doc():
    return mock.Mock()

def test_add_keys(doc):
    doc.add('a')
    assert str(doc) == 'a'
    doc.add('b')
    assert str(doc) == 'ab'

def test_home(full_doc):
    pass

def test_bksp(full_doc):
    full_doc.bksp()
    assert str(full_doc) == sample_text[:-1]
    full_doc.bksp()
    assert str(full_doc) == sample_text[:-2]

def test_handle_literal(mock_doc):
    answers.Document.handle(mock_doc, 'a')
    mock_doc.add.assert_called_once_with('a')
    answers.Document.handle(mock_doc, '%')
    mock_doc.add.assert_called_with('%')

def test_handle_bksp(mock_doc):
    answers.Document.handle(mock_doc, '<BACKSPACE>')
    mock_doc.bksp.assert_called_once_with()

def test_handle_newline(mock_doc):
    answers.Document.handle(mock_doc, '<Ctrl-j>')
    mock_doc.add.assert_called_once_with('\n')

def test_lines(full_doc):
    lines = full_doc.lines
    assert len(lines) == 5

def test_initial_cursor(full_doc):
    cursor = full_doc.cursor
    assert cursor[0] == 4
    assert cursor[1] == 43

def test_jump_left_word(full_doc):
    full_doc.move_word(answers.document.Dir.LEFT)
    cursor = full_doc.cursor
    assert str(full_doc) == sample_text
    assert cursor[0] == 4
    assert cursor[1] == 38

def test_jump_right_word(full_doc):
    full_doc.move_word(answers.document.Dir.RIGHT)
    cursor = full_doc.cursor
    assert str(full_doc) == sample_text
    assert cursor[0] == 4
    assert cursor[1] == 43

