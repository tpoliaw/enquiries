from answers import Document
from answers import document
import pytest
from unittest import mock

@pytest.fixture
def doc():
    return Document()

sample_text = """this is a piece of sample text containing varying
line
lengths.

And new paragraphs also with     multiple lines"""


@pytest.fixture
def full_doc():
    return Document(sample_text, 58)

@pytest.fixture
def mock_doc():
    return mock.Mock()

def test_add_keys(doc):
    doc.add('a')
    assert str(doc) == 'a'
    doc.add('b')
    assert str(doc) == 'ab'


def test_bksp(full_doc):
    full_doc.bksp()
    assert str(full_doc) == sample_text[:57] + sample_text[58:]
    full_doc.bksp()
    assert str(full_doc) == sample_text[:56] + sample_text[58:]

def test_handle_literal(mock_doc):
    Document.handle(mock_doc, 'a')
    mock_doc.add.assert_called_once_with('a')
    Document.handle(mock_doc, '%')
    mock_doc.add.assert_called_with('%')

def test_handle_bksp(mock_doc):
    Document.handle(mock_doc, '<BACKSPACE>')
    mock_doc.bksp.assert_called_once_with()

def test_handle_newline(mock_doc):
    Document.handle(mock_doc, '<Ctrl-j>')
    mock_doc.add.assert_called_once_with('\n')

def test_lines(full_doc):
    lines = full_doc.lines
    assert len(lines) == 5

def test_initial_cursor(full_doc):
    cursor = full_doc.cursor
    assert cursor[0] == 2
    assert cursor[1] == 3

def test_jump_left_word(full_doc):
    full_doc.move_word(document.Dir.LEFT)
    cursor = full_doc.cursor
    assert str(full_doc) == sample_text
    assert cursor[0] == 2
    assert cursor[1] == 0

def test_jump_right_word(full_doc):
    full_doc.move_word(document.Dir.RIGHT)
    cursor = full_doc.cursor
    assert str(full_doc) == sample_text
    assert cursor[0] == 2
    assert cursor[1] == 7

