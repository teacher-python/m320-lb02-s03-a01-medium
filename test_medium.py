""" Tests for the class Medium """
import pytest

from fixtures import MediumDummy, skip_if_incomplete, skip_if_missing
from medium import Medium


def test_medium_is_abstract():
    """
    Medium is an abstract class and cannot be instantiated.
    The check on 'abstract' in the message makes sure the TypeError
    is not caused by a constructor without parameters.
    """
    with pytest.raises(TypeError, match='abstract'):
        Medium('Bohemian Rhapsody', 354)


@pytest.mark.parametrize('attr', ['title', 'length'])
def test_medium_private_attributes(attr):
    """ each attribute is stored in a private attribute (e.g. _title) """
    obj = MediumDummy('Bohemian Rhapsody', 354)
    assert '_' + attr in vars(obj)
    assert attr not in vars(obj)


@pytest.mark.parametrize('attr', ['title', 'length'])
def test_medium_properties(attr):
    """ Medium has a property with a setter for each attribute """
    prop = vars(Medium).get(attr)
    assert isinstance(prop, property)
    assert prop.fget is not None
    assert prop.fset is not None


@pytest.mark.parametrize('attr, value', [
    ('title', 'A'),
    ('title', 'Africa'),
    ('length', 1),
    ('length', 36000)
])
def test_medium_setters_valid(attr, value):
    """ the setters accept valid values (incl. the limits) """
    skip_if_incomplete(Medium, [attr])
    obj = MediumDummy('Bohemian Rhapsody', 354)
    skip_if_incomplete(Medium, [attr], obj)
    setattr(obj, attr, value)
    assert getattr(obj, attr) == value


@pytest.mark.parametrize('attr, value', [
    ('title', ''),
    ('title', None),
    ('length', 0),
    ('length', 36001),
    ('length', None)
])
def test_medium_setters_invalid(attr, value):
    """ the setters raise a ValueError for invalid values and keep the old value """
    skip_if_incomplete(Medium, [attr])
    obj = MediumDummy('Bohemian Rhapsody', 354)
    skip_if_incomplete(Medium, [attr], obj)
    old = getattr(obj, attr)
    with pytest.raises(ValueError):
        setattr(obj, attr, value)
    assert getattr(obj, attr) == old


def test_medium_abstract_calc_duration():
    """ calc_duration is declared as abstract method in Medium """
    assert 'calc_duration' in getattr(Medium, '__abstractmethods__', set())


def test_medium_create_full():
    """ the constructor of Medium sets title and length """
    obj = MediumDummy('Bohemian Rhapsody', 354)
    assert obj.title == 'Bohemian Rhapsody'
    assert obj.length == 354


@pytest.mark.parametrize('title', ['', None])
def test_medium_invalid_title(title):
    """ an empty or missing title raises a ValueError """
    with pytest.raises(ValueError):
        MediumDummy(title, 354)


@pytest.mark.parametrize('length', [0, 36001, None])
def test_medium_invalid_length(length):
    """ a length outside 1 ... 36000 raises a ValueError """
    with pytest.raises(ValueError):
        MediumDummy('Bohemian Rhapsody', length)


def test_medium_format_duration():
    """ format_duration returns the length as mm:ss """
    skip_if_missing(Medium, 'format_duration')
    assert MediumDummy('Africa', 295).format_duration() == '04:55'
    assert MediumDummy('Intro', 9).format_duration() == '00:09'


def test_medium_equal():
    """ two media with the same title and length are equal """
    skip_if_missing(Medium, '__eq__')
    assert MediumDummy('Africa', 295) == MediumDummy('Africa', 295)
    assert MediumDummy('Africa', 295) != MediumDummy('Africa', 296)
