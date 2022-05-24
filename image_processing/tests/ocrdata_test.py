import math

import pytest

from ..ocrdata import *


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
            Word().update_attr(value[0], value[1])
    for value in type_error_values:
        with pytest.raises(TypeError):
            Word().update_attr(value[0], value[1])
    for value in value_error_values:
        with pytest.raises(ValueError):
            Word().update_attr(value[0], value[1])
    for value in good_values:
        assert Word().update_attr(value[0], value[1]) is None

def test_word_get_center():
    test_word_values = [
        [
            {  # Zero-width word at origin
                'top': 0,
                'left': 0,
                'width': 0,
                'height': 0,
            }, (0.0, 0.0)  # Expected value
        ],
        [
            {
                'top': 54,
                'left': 27,
                'width': 75,
                'height': 20,
            }, (64.5, 64.0)
        ],
        [
            {
                'top': 356,
                'left': 954,
                'width': 63,
                'height': 17,
            }, (985.5, 364.5)
        ]
    ]

    for test_value in test_word_values:
        test_word = Word()
        test_attributes = test_value[0].keys()
        for attribute in test_attributes:
            test_word.update_attr(attribute, test_value[0].get(attribute))
        assert test_word.get_center() == test_value[1]

