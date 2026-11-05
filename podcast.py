""" Provides the class Podcast """
from medium import Medium


class Podcast(Medium):
    """
    a podcast episode as medium of a playlist

    Attributes
    ----------
    episode : int
        the number of the episode (at least 1)
    ad_seconds : int
        the length of the advertisements in seconds (0 ... 600)
    """

    def __init__(self, title, length, episode, ad_seconds=0):
        """
        Creates a new podcast episode
        :param title: the title of the podcast
        :param length: the length of the podcast in seconds
        :param episode: the number of the episode
        :param ad_seconds: the length of the advertisements in seconds
        """
        super().__init__(title, length)
        self.episode = episode
        self.ad_seconds = ad_seconds

    def calc_duration(self):
        """ Calculate the duration of the podcast incl. advertisements in minutes """
        return (self.length + self.ad_seconds) / 60

    @property
    def episode(self):
        """ Get the number of the episode """
        return self._episode

    @episode.setter
    def episode(self, value):
        """ Set the number of the episode """
        if not isinstance(value, int) or value < 1:
            raise ValueError
        self._episode = value

    @property
    def ad_seconds(self):
        """ Get the length of the advertisements in seconds """
        return self._ad_seconds

    @ad_seconds.setter
    def ad_seconds(self, value):
        """ Set the length of the advertisements in seconds """
        if not isinstance(value, int) or not 0 <= value <= 600:
            raise ValueError
        self._ad_seconds = value
