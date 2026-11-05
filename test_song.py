""" Tests for the class Song """
import pytest

from fixtures import skip_if_incomplete, skip_if_missing
from medium import Medium
from song import Song


def test_song_create_full():
    """ A song can be created with all arguments """
    song = Song('Bohemian Rhapsody', 354, 'Queen', 72)
    assert song.title == 'Bohemian Rhapsody'
    assert song.length == 354
    assert song.artist == 'Queen'
    assert song.bpm == 72


def test_song_create_default():
    """ A song created without bpm gets the default value 120 """
    song = Song('Africa', 295, 'Toto')
    assert song.artist == 'Toto'
    assert song.bpm == 120


@pytest.mark.parametrize('artist', ['', None])
def test_song_invalid_artist(artist):
    """ An empty or missing artist raises a ValueError """
    with pytest.raises(ValueError):
        Song('Africa', 295, artist)


@pytest.mark.parametrize('bpm', [39, 241, None])
def test_song_invalid_bpm(bpm):
    """ A bpm outside 40 ... 240 raises a ValueError """
    with pytest.raises(ValueError):
        Song('Africa', 295, 'Toto', bpm)


@pytest.mark.parametrize('attr', ['artist', 'bpm'])
def test_song_private_attributes(attr):
    """ each attribute is stored in a private attribute (e.g. _artist) """
    obj = Song('Africa', 295, 'Toto', 92)
    assert '_' + attr in vars(obj)
    assert attr not in vars(obj)


@pytest.mark.parametrize('attr', ['artist', 'bpm'])
def test_song_properties(attr):
    """ Song has a property with a setter for each attribute """
    prop = vars(Song).get(attr)
    assert isinstance(prop, property)
    assert prop.fget is not None
    assert prop.fset is not None


@pytest.mark.parametrize('attr, value', [
    ('artist', 'A'),
    ('artist', 'Queen'),
    ('bpm', 40),
    ('bpm', 240)
])
def test_song_setters_valid(attr, value):
    """ the setters accept valid values (incl. the limits) """
    skip_if_incomplete(Song, [attr])
    obj = Song('Africa', 295, 'Toto', 92)
    skip_if_incomplete(Song, [attr], obj)
    setattr(obj, attr, value)
    assert getattr(obj, attr) == value


@pytest.mark.parametrize('attr, value', [
    ('artist', ''),
    ('artist', None),
    ('bpm', 39),
    ('bpm', 241),
    ('bpm', None)
])
def test_song_setters_invalid(attr, value):
    """ the setters raise a ValueError for invalid values and keep the old value """
    skip_if_incomplete(Song, [attr])
    obj = Song('Africa', 295, 'Toto', 92)
    skip_if_incomplete(Song, [attr], obj)
    old = getattr(obj, attr)
    with pytest.raises(ValueError):
        setattr(obj, attr, value)
    assert getattr(obj, attr) == old


@pytest.mark.parametrize('length, expected', [
    (60, 1.0),
    (295, 295 / 60),
    (36000, 600.0)
])
def test_song_calc_duration(length, expected):
    """ calc_duration returns the length in minutes: length / 60 """
    skip_if_incomplete(Song, ['length'])
    song = Song('Africa', length, 'Toto')
    skip_if_incomplete(Song, ['length'], song)
    assert song.calc_duration() == pytest.approx(expected)


def test_song_subclass_of_medium():
    """ Song inherits from the abstract class Medium """
    assert issubclass(Song, Medium)
    assert 'calc_duration' in vars(Song)


def test_song_missing_arguments():
    """
    creating a Song without the required arguments raises a TypeError,
    but it works with all required arguments
    """
    assert Song('Africa', 295, 'Toto') is not None
    with pytest.raises(TypeError):
        Song('Africa', 295)


def test_song_genre():
    """ the genre of a song is empty by default and can be changed """
    skip_if_missing(Song, 'genre')
    song = Song('Africa', 295, 'Toto')
    assert song.genre == ''
    song.genre = 'Rock'
    assert song.genre == 'Rock'
