""" Provides the class Audiobook """
from medium import Medium


class Audiobook(Medium):
    """
    an audiobook as medium of a playlist

    Attributes
    ----------
    narrator : str
        the narrator of the audiobook (at least 1 character)
    speed : float
        the playback speed of the audiobook (0.5 ... 2.0)
    """

    def __init__(self, title, length, narrator, speed=1.0):
        """
        Creates a new audiobook
        :param title: the title of the audiobook
        :param length: the length of the audiobook in seconds
        :param narrator: the narrator of the audiobook
        :param speed: the playback speed of the audiobook
        """
        super().__init__(title, length)
        self.narrator = narrator
        self.speed = speed

    def calc_duration(self):
        """ Calculate the duration of the audiobook at the given speed in minutes """
        return self.length / self.speed / 60

    @property
    def narrator(self):
        """ Get the narrator of the audiobook """
        return self._narrator

    @narrator.setter
    def narrator(self, value):
        """ Set the narrator of the audiobook """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError
        self._narrator = value

    @property
    def speed(self):
        """ Get the playback speed of the audiobook """
        return self._speed

    @speed.setter
    def speed(self, value):
        """ Set the playback speed of the audiobook """
        if not isinstance(value, (int, float)) or not 0.5 <= value <= 2.0:
            raise TypeError
        self._speed = value
