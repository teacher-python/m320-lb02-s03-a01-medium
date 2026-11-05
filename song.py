""" Provides the class Song """
from medium import Medium


class Song(Medium):
    """
    a song as medium of a playlist

    Attributes
    ----------
    artist : str
        the artist of the song (at least 1 character)
    bpm : int
        the beats per minute of the song (40 ... 240)
    """

    def __init__(self, title, length, artist, bpm=120):
        """
        Creates a new song
        :param title: the title of the song
        :param length: the length of the song in seconds
        :param artist: the artist of the song
        :param bpm: the beats per minute of the song
        """
        super().__init__(title, length)
        self.artist = artist
        self.bpm = bpm

    def calc_duration(self):
        """ Calculate the duration of the song in minutes """
        return self.length / 60

    @property
    def artist(self):
        """ Get the artist of the song """
        return self._artist

    @artist.setter
    def artist(self, value):
        """ Set the artist of the song """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError
        self._artist = value

    @property
    def bpm(self):
        """ Get the beats per minute of the song """
        return self._bpm

    @bpm.setter
    def bpm(self, value):
        """ Set the beats per minute of the song """
        if not isinstance(value, int) or not 40 <= value <= 240:
            raise TypeError
        self._bpm = value
