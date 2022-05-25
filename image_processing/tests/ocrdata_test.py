from ..ocrdata import *
import pytest


@pytest.fixture
def valid_test_words():
    test_word_values = [
        {  # Zero-width word at origin
            'top': 0,
            'left': 0,
            'width': 0,
            'height': 0,
            'text': 'test_word_1',
        },
        {
            'top': 54,
            'left': 27,
            'width': 75,
            'height': 20,
            'text': 'test_word_2',
        },
        {
            'top': 356,
            'left': 954,
            'width': 63,
            'height': 17,
            'text': 'test_word_3',
        },
        {
            'top': 799,
            'left': 1426,
            'width': 111,
            'height': 22,
            'text': 'test_word_4',
        }
    ]

    word_list = []
    for word in test_word_values:
        test_word = Word()  # Make a new word
        test_attributes = word.keys()
        for attribute in test_attributes:
            test_word.update_attr(attribute, word.get(attribute))  # Update new word with every attribute in the list
        word_list.append(test_word)  # Add the updated word to the word list
    return word_list


def test_word_get_attr(valid_test_words):
    for test_word in valid_test_words:
        with pytest.raises(KeyError):
            test_word.get_attr(None)
            test_word.get_attr(0)
            test_word.get_attr(0.0)
            test_word.get_attr(False)

    assert valid_test_words[0].get_attr('text') == 'test_word_1'
    assert valid_test_words[1].get_attr('top') == 54
    assert valid_test_words[2].get_attr('left') == 954
    assert valid_test_words[3].get_attr('width') == 111


def test_word_update_attr():
    key_error_values = [
        ('', ''),
        ('', False),
        ('', 0),
        ('', 0.0),
        ('', None),
        (0, ''),
        (0.0, ''),
        (False, ''),
        (None, ''),
        ('levle', 1),
        ('line-num', 2),
        ('txet', 'testtext'),
    ]

    type_error_values = [
        ('level', ''),
        ('line_num', 4.2),
        ('width', True),
        ('height', None),
        ('conf', False),
        ('conf', ''),
        ('conf', None),
        ('text', 0),
        ('text', 0.0),
        ('text', True),
        ('text', None),
    ]

    value_error_values = [
        ('conf', -23.244),
        ('conf', -0.32),
        ('conf', 143),
        ('level', -1),
        ('top', -47),
        ('width', -10),
    ]

    good_values = [
        ('level', 3),
        ('left', 10),
        ('conf', 78.23),
        ('conf', -1),
        ('text', 'testtext'),

    ]

    for value in key_error_values:
        with pytest.raises(KeyError):
            Word().update_attr(value[0], value[1])  # Use tuple as the two args for the update_attr method
    for value in type_error_values:
        with pytest.raises(TypeError):
            Word().update_attr(value[0], value[1])
    for value in value_error_values:
        with pytest.raises(ValueError):
            Word().update_attr(value[0], value[1])
    for value in good_values:
        assert Word().update_attr(value[0], value[1]) is None  # Method has no return statement, so should return none


def test_word_get_center(valid_test_words):
    assert valid_test_words[0].get_center() == (0.0, 0.0)
    assert valid_test_words[1].get_center() == (64.5, 64.0)
    assert valid_test_words[2].get_center() == (985.5, 364.5)
    assert valid_test_words[3].get_center() == (1481.5, 810)


def test_word_distance_between(valid_test_words):
    # Testing values rounded down to two decimal points
    assert round(valid_test_words[0].distance_between(valid_test_words[1]), 2) == 90.86
    assert round(valid_test_words[0].distance_between(valid_test_words[2]), 2) == 1050.75
    assert round(valid_test_words[0].distance_between(valid_test_words[3]), 2) == 1688.47
    assert round(valid_test_words[1].distance_between(valid_test_words[2]), 2) == 968.78
    assert round(valid_test_words[1].distance_between(valid_test_words[3]), 2) == 1601.38
    assert round(valid_test_words[2].distance_between(valid_test_words[3]), 2) == 666.7


def test_wordlist_append_get(valid_test_words):
    test_wordlist = WordList()

    duplicate_word_1 = Word()
    duplicate_word_2 = Word()
    duplicate_word_1.update_attr('text', 'duplicate_text')
    duplicate_word_2.update_attr('text', 'duplicate_text')

    test_wordlist.append(duplicate_word_1)
    test_wordlist.append(duplicate_word_2)

    for test_word in valid_test_words:
        test_wordlist.append(test_word)

    assert test_wordlist.get_words('nonexistent_word') is None
    assert test_wordlist.get_words(0) is None
    assert test_wordlist.get_words(0.0) is None
    assert test_wordlist.get_words(False) is None
    assert [valid_test_words[0]] == test_wordlist.get_words(valid_test_words[0].get_attr('text'))
    assert [valid_test_words[1]] == test_wordlist.get_words(valid_test_words[1].get_attr('text'))
    assert [valid_test_words[2]] == test_wordlist.get_words(valid_test_words[2].get_attr('text'))
    assert [valid_test_words[3]] == test_wordlist.get_words(valid_test_words[3].get_attr('text'))
    assert [duplicate_word_1, duplicate_word_2] == test_wordlist.get_words(duplicate_word_1.get_attr('text'))
