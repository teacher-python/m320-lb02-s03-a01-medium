""" Tests for the class Audiobook """
import pytest

from fixtures import skip_if_incomplete, skip_if_missing
from medium import Medium
from audiobook import Audiobook


def test_audiobook_create_full():
    """ An audiobook can be created with all arguments """
    book = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes', 1.5)
    assert book.title == 'Der Steppenwolf'
    assert book.length == 36000
    assert book.narrator == 'Ulrich Matthes'
    assert book.speed == 1.5


def test_audiobook_create_default():
    """ An audiobook created without speed gets the default value 1.0 """
    book = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes')
    assert book.narrator == 'Ulrich Matthes'
    assert book.speed == 1.0


@pytest.mark.parametrize('narrator', ['', None])
def test_audiobook_invalid_narrator(narrator):
    """ An empty or missing narrator raises a ValueError """
    with pytest.raises(ValueError):
        Audiobook('Der Steppenwolf', 36000, narrator)


@pytest.mark.parametrize('speed', [0.49, 2.01, None])
def test_audiobook_invalid_speed(speed):
    """ A speed outside 0.5 ... 2.0 raises a ValueError """
    with pytest.raises(ValueError):
        Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes', speed)


@pytest.mark.parametrize('attr', ['narrator', 'speed'])
def test_audiobook_private_attributes(attr):
    """ each attribute is stored in a private attribute (e.g. _narrator) """
    obj = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes', 1.5)
    assert '_' + attr in vars(obj)
    assert attr not in vars(obj)


@pytest.mark.parametrize('attr', ['narrator', 'speed'])
def test_audiobook_properties(attr):
    """ Audiobook has a property with a setter for each attribute """
    prop = vars(Audiobook).get(attr)
    assert isinstance(prop, property)
    assert prop.fget is not None
    assert prop.fset is not None


@pytest.mark.parametrize('attr, value', [
    ('narrator', 'N'),
    ('narrator', 'Gert Westphal'),
    ('speed', 0.5),
    ('speed', 2.0)
])
def test_audiobook_setters_valid(attr, value):
    """ the setters accept valid values (incl. the limits) """
    skip_if_incomplete(Audiobook, [attr])
    obj = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes', 1.5)
    skip_if_incomplete(Audiobook, [attr], obj)
    setattr(obj, attr, value)
    assert getattr(obj, attr) == value


@pytest.mark.parametrize('attr, value', [
    ('narrator', ''),
    ('narrator', None),
    ('speed', 0.49),
    ('speed', 2.01),
    ('speed', None)
])
def test_audiobook_setters_invalid(attr, value):
    """ the setters raise a ValueError for invalid values and keep the old value """
    skip_if_incomplete(Audiobook, [attr])
    obj = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes', 1.5)
    skip_if_incomplete(Audiobook, [attr], obj)
    old = getattr(obj, attr)
    with pytest.raises(ValueError):
        setattr(obj, attr, value)
    assert getattr(obj, attr) == old


@pytest.mark.parametrize('length, speed, expected', [
    (3600, 1.0, 60.0),
    (3600, 2.0, 30.0),
    (3600, 0.5, 120.0),
    (1000, 1.5, 1000 / 1.5 / 60)
])
def test_audiobook_calc_duration(length, speed, expected):
    """ calc_duration returns the duration at the given speed in minutes: length / speed / 60 """
    skip_if_incomplete(Audiobook, ['length', 'speed'])
    book = Audiobook('Der Steppenwolf', length, 'Ulrich Matthes', speed)
    skip_if_incomplete(Audiobook, ['length', 'speed'], book)
    assert book.calc_duration() == pytest.approx(expected)


def test_audiobook_subclass_of_medium():
    """ Audiobook inherits from the abstract class Medium """
    assert issubclass(Audiobook, Medium)
    assert 'calc_duration' in vars(Audiobook)


def test_audiobook_missing_arguments():
    """
    creating a Audiobook without the required arguments raises a TypeError,
    but it works with all required arguments
    """
    assert Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes') is not None
    with pytest.raises(TypeError):
        Audiobook('Der Steppenwolf', 36000)


def test_audiobook_chapters():
    """ an audiobook has at least 1 chapter, the default is 1 """
    skip_if_missing(Audiobook, 'chapters')
    book = Audiobook('Der Steppenwolf', 36000, 'Ulrich Matthes')
    assert book.chapters == 1
    book.chapters = 12
    assert book.chapters == 12
    with pytest.raises(ValueError):
        book.chapters = 0
