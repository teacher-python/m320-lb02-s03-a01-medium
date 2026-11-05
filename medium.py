""" Provides the abstract class Medium for the media of a playlist """
from abc import ABC, abstractmethod


class Medium(ABC):
    """
    an abstract medium (song, podcast, audiobook) of a playlist

    Attributes
    ----------
    title : str
        the title of the medium (at least 1 character)
    length : int
        the length of the medium in seconds (1 ... 36000)
    """

    def __init__(self, title, length):
        """
        Initializes the parameters
        :param title: the title of the medium
        :param length: the length of the medium in seconds
        """
        self.title = title
        self.length = length

    @property
    def title(self):
        """ Get the title of the medium """
        return self._title

    @title.setter
    def title(self, value):
        """ Set the title of the medium """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError
        self._title = value

    @property
    def length(self):
        """ Get the length of the medium in seconds """
        return self._length

    @length.setter
    def length(self, value):
        """ Set the length of the medium in seconds """
        if not isinstance(value, int) or not 1 <= value <= 36000:
            raise TypeError
        self._length = value

    @abstractmethod
    def calc_duration(self):
        """ Calculate the duration of the medium in minutes """
        pass
