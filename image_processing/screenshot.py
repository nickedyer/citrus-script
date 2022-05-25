import cv2
import pyautogui
import numpy as np


class ScreenshotHelper:
    """
    Class that aids in getting a screenshot of the screen from pyautogui. Contains methods to get a new screenshot
    and apply brightness and contrast filters to it, as well as inverting the image.
    """

    def __init__(self):
        self._image = np.array(0)
        self._unedited_image = np.array(0)

    def get_screenshot(self):
        """
        Captures a black and white screenshot.
        """
        new_screenshot = pyautogui.screenshot()
        bw_screenshot = cv2.cvtColor(np.array(new_screenshot), cv2.COLOR_BGR2GRAY)  # Convert screenshot to Grayscale
        self._image = bw_screenshot
        self._unedited_image = bw_screenshot

    def invert(self):
        """
        Inverts the currently stored image.
        """
        self._image = cv2.bitwise_not(self._image)

    def crop(self, crop_tl, crop_br):
        """
        Crops the current image to a box defined by the pair of points crop_x and crop_y. crop_tl is the top-left
        corner of the new image, and crop_br is the bottom-right corner.

        :param crop_x: tuple of the top-left corner
        :param crop_y: tuple of the bottom-right corner
        """
        raise NotImplementedError('The crop method has not been implemented yet.')

    def adjust_contrast_brightness(self, alpha, beta):
        """
        Adjusts the brightness and contrast of the current image.

        | Contrast is adjusted using alpha, a multiplier for the current image where:
        | a == 1: no contrast change
        | a > 1: increase contrast
        | a < 1: decrease contrast

        | Brightness is adjusting using beta, which adds or subtracts linearly after alpha is applied:
        | beta == 0: no brightness change
        | beta > 0: increase brightnesss
        |  beta < 0: decrease brightnesss
        :param alpha: contrast adjustment
        :param beta: brightness adjustment
        """
        info = np.iinfo(self._image.dtype)  # Get the information of the incoming image type
        orig_type = self._image.dtype
        # Change the numpy array from the incoming type to a float64 and normalize it from 0 to 1 with 0 being black
        # and 1 being white.
        self._image = self._image.astype(np.float64) / info.max
        self._image *= 255  # Change scale from 0-1 to 0-255 to match 8-bit B&W
        # Apply contrast and brightness values and cap resulting pixels at either 0 or 255
        self._image = np.clip((self._image * alpha) + beta, 0, 255)
        self._image = self._image.astype(orig_type)  # Convert the image back to its original type

    def reset_screenshot(self):
        """
        Resets the screenshot back to its original state before any inversion or brightness/contrast changes.
        """
        self._image = self._unedited_image
