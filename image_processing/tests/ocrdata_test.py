from ..ocrdata import *
import pytest


def test_word_update():
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


@pytest.fixture
def valid_test_words():
    test_word_values = [
        {  # Zero-width word at origin
            'top': 0,
            'left': 0,
            'width': 0,
            'height': 0,
        },
        {
            'top': 54,
            'left': 27,
            'width': 75,
            'height': 20,
        },
        {
            'top': 356,
            'left': 954,
            'width': 63,
            'height': 17,
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


def test_word_get_center(valid_test_words):
    assert valid_test_words[0].get_center() == (0.0, 0.0)
    assert valid_test_words[1].get_center() == (64.5, 64.0)
    assert valid_test_words[2].get_center() == (985.5, 364.5)


def test_word_distance_between(valid_test_words):
    assert round(valid_test_words[0].distance_between(valid_test_words[1]), 2) == 90.86
    assert round(valid_test_words[1].distance_between(valid_test_words[2]), 2) == 968.78
    assert round(valid_test_words[2].distance_between(valid_test_words[0]), 2) == 1050.75
