from answers.document import Document
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

def test_handle(mock_doc):
    Document.handle(mock_doc, 'a')
    mock_doc.add.assert_called_with('a')
    Document.handle(mock_doc, '<SPACE>')
    mock_doc.add.assert_called_with(' ')
    Document.handle(mock_doc, '<BACKSPACE>')
    mock_doc.bksp.assert_called_with()
    Document.handle(mock_doc, '<DELETE>')
    mock_doc.bksp.assert_called_with(document.Dir.RIGHT)

def test_bksp(full_doc):
    full_doc.bksp()
    assert str(full_doc) == sample_text[:57] + sample_text[58:]
    full_doc.bksp()
    assert str(full_doc) == sample_text[:56] + sample_text[58:]

def test_del(full_doc):
    full_doc.bksp(document.Dir.RIGHT)
    assert str(full_doc) == sample_text[:58] + sample_text[59:]
    full_doc.bksp(document.Dir.RIGHT)
    assert str(full_doc) == sample_text[:58] + sample_text[60:]

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

def test_move_cursor_left(full_doc):
    cursor = full_doc.cursor
    full_doc.move_cursor(direction=document.Dir.LEFT)
    assert full_doc.cursor.column == 2
    assert full_doc.cursor.row == 2

def test_move_cursor_right(full_doc):
    cursor = full_doc.cursor
    full_doc.move_cursor(direction=document.Dir.RIGHT)
    assert full_doc.cursor.column == 4
    assert full_doc.cursor.row == 2
    assert str(full_doc) == sample_text

def test_move_cursor_up(full_doc):
    cursor = full_doc.cursor
    full_doc.move_cursor(direction=document.Dir.UP)
    assert full_doc.cursor.column == 3
    assert full_doc.cursor.row == 1
    assert str(full_doc) == sample_text

def test_move_up_from_top():
    doc = Document(sample_text, 0)
    c = doc.cursor
    doc.move_cursor(document.Dir.UP)
    assert c == doc.cursor
    assert str(doc) == sample_text

def test_move_cursor_down(full_doc):
    cursor = full_doc.cursor
    full_doc.move_cursor(direction=document.Dir.DOWN)
    assert full_doc.cursor.column == 0
    assert full_doc.cursor.row == 3
    assert str(full_doc) == sample_text

def test_move_down_from_bottom():
    doc = Document(sample_text, 100)
    c = doc.cursor
    doc.move_cursor(document.Dir.DOWN)
    assert c == doc.cursor
    assert str(doc) == sample_text

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

def test_word_left_from_spaces():
    doc = Document(sample_text, 95)
    doc.move_word(document.Dir.LEFT)
    assert doc.cursor.column == 24
    assert doc.cursor.row  == 4

def test_word_right_from_spaces():
    doc = Document(sample_text, 95)
    doc.move_word(document.Dir.RIGHT)
    assert doc.cursor.column == 41
    assert doc.cursor.row  == 4


# ==============================================
# Tests for document helper functions
# ==============================================

@pytest.fixture
def text():
    return ['this is a single line that should be split over many lines when wrapped']

def test_wrap(text):
    print(text)
    lines, cursor = document._wrap(text, document.Cursor(0, len(text[0])), 16)
    print(cursor)
    assert list(lines) == ['this is a ', 'single line ', 'that should be ', 'split over many', 'lines when ', 'wrapped']
    assert cursor.row == 5
    assert cursor.column == 6

def test_split_line_wrap(text):
    lines, cursor = document._wrap(text, document.Cursor(0, 30), 16)
    assert list(lines) == ['this is a ', 'single line ', 'that should be ', 'split over many', 'lines when ', 'wrapped']
    assert cursor.row == 2
    assert cursor.column == 8

def test_split_with_empty_line():
    lines, cursor = document._wrap(['first line', ''], document.Cursor(1,0), 15)
    assert list(lines) == ['first line', '']
    assert cursor.row == 1
    assert cursor.column == 0

def test_current_word():
    assert document._current_word(['one', 'two', 'three'], 5) == (1,2)
    with pytest.raises(ValueError):
        document._current_word(['one'], 8)
