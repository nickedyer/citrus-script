import math


class Word:
    """
    Class that defines one recognized word. Contains all the attributes about the word and contains methods to
    compare words to each other in various different ways.
    """

    def __init__(self):
        # Attributes that a word can have. These are the same names as the attributes that Python-tesseract produces
        # with its image_get_data() function. The types of these values cannot change as enforced by update_attr().
        self._attributes = {
            'level': 0,
            'page_num': 0,
            'block_num': 0,
            'par_num': 0,
            'line_num': 0,
            'word_num': 0,
            'left': 0,
            'top': 0,
            'width': 0,
            'height': 0,
            'conf': 0.0,
            'text': '',
        }

    def get_attr(self, attribute):
        """
        Returns the value of a given attribute. Raises KeyError if given an attribute not in the Word object.
        :param attribute:
        :return:
        """
        if attribute in self._attributes:
            return self._attributes.get(attribute)
        else:
            raise KeyError('{0} is not an attribute for class Word'.format(attribute))

    def update_attr(self, attribute, value):
        """
        Update the attribute of a word to a new value. Throws KeyError if the key does not exist. Throws TypeError if
        the new type does not match the old one. All numeric values must be 0 or positive apart from 'conf' that can be -1 or from 0-100

        :param attribute: attribute to be changed
        :param value: new value of the attribute
        :return: the new updated word object
        """

        if attribute not in self._attributes:
            raise KeyError()

        else:
            old_value = self._attributes.get(attribute)

            # First check if the attribute is 'conf' as it can have two different types
            if attribute == 'conf':
                if type(value) != type(old_value) and (type(value) != float and type(value) != int):
                    raise TypeError()
                elif (value > 100 or value < 0) and value != -1:
                    raise ValueError()
                else:
                    self._attributes[attribute] = value  # Write value if conf check passes
            elif type(value) != type(old_value):
                raise TypeError('Attribute {attr} must be of type {type}'.format(attr=attribute, type=type(old_value)))
            elif attribute != 'text' and value < 0:
                raise ValueError('Numeric values other than confidence (conf) must be positive')
            else:
                self._attributes[attribute] = value  # Write value if remaining type checks pass

    def get_center(self):
        """
        Get the coordinates (px) of the center of the word in relation to the original image given to Tesseract.
        Coordinates originate at the top-left of the image, with x increasing from left to right,
        and y increasing from top to bottom.

        :return: coordinates as a tuple (x,y)
        """
        return (self._attributes.get('left') + (self._attributes.get('width') / 2),
                self._attributes.get('top') + (self._attributes.get('height') / 2))

    def distance_between(self, word):
        """
        Get the distance between this word object and another word object in pixels.

        :param word: second word to find the distance between
        :return: distance in pixels
        """
        return math.dist(self.get_center(), word.get_center())
