""" Tests for the class Podcast """
import pytest

from fixtures import skip_if_incomplete, skip_if_missing
from medium import Medium
from podcast import Podcast


def test_podcast_create_full():
    """ A podcast can be created with all arguments """
    podcast = Podcast('Echo der Zeit', 1800, 12, 90)
    assert podcast.title == 'Echo der Zeit'
    assert podcast.length == 1800
    assert podcast.episode == 12
    assert podcast.ad_seconds == 90


def test_podcast_create_default():
    """ A podcast created without ad_seconds gets the default value 0 """
    podcast = Podcast('Echo der Zeit', 1800, 1)
    assert podcast.episode == 1
    assert podcast.ad_seconds == 0


@pytest.mark.parametrize('episode', [0, -1, None])
def test_podcast_invalid_episode(episode):
    """ An episode below 1 raises a ValueError """
    with pytest.raises(ValueError):
        Podcast('Echo der Zeit', 1800, episode)


@pytest.mark.parametrize('ad_seconds', [-1, 601, None])
def test_podcast_invalid_ad_seconds(ad_seconds):
    """ ad_seconds outside 0 ... 600 raises a ValueError """
    with pytest.raises(ValueError):
        Podcast('Echo der Zeit', 1800, 12, ad_seconds)


@pytest.mark.parametrize('attr', ['episode', 'ad_seconds'])
def test_podcast_private_attributes(attr):
    """ each attribute is stored in a private attribute (e.g. _episode) """
    obj = Podcast('Echo der Zeit', 1800, 12, 90)
    assert '_' + attr in vars(obj)
    assert attr not in vars(obj)


@pytest.mark.parametrize('attr', ['episode', 'ad_seconds'])
def test_podcast_properties(attr):
    """ Podcast has a property with a setter for each attribute """
    prop = vars(Podcast).get(attr)
    assert isinstance(prop, property)
    assert prop.fget is not None
    assert prop.fset is not None


@pytest.mark.parametrize('attr, value', [
    ('episode', 1),
    ('episode', 999),
    ('ad_seconds', 0),
    ('ad_seconds', 600)
])
def test_podcast_setters_valid(attr, value):
    """ the setters accept valid values (incl. the limits) """
    skip_if_incomplete(Podcast, [attr])
    obj = Podcast('Echo der Zeit', 1800, 12, 90)
    skip_if_incomplete(Podcast, [attr], obj)
    setattr(obj, attr, value)
    assert getattr(obj, attr) == value


@pytest.mark.parametrize('attr, value', [
    ('episode', 0),
    ('episode', -1),
    ('episode', None),
    ('ad_seconds', -1),
    ('ad_seconds', 601),
    ('ad_seconds', None)
])
def test_podcast_setters_invalid(attr, value):
    """ the setters raise a ValueError for invalid values and keep the old value """
    skip_if_incomplete(Podcast, [attr])
    obj = Podcast('Echo der Zeit', 1800, 12, 90)
    skip_if_incomplete(Podcast, [attr], obj)
    old = getattr(obj, attr)
    with pytest.raises(ValueError):
        setattr(obj, attr, value)
    assert getattr(obj, attr) == old


@pytest.mark.parametrize('length, ad_seconds, expected', [
    (1800, 0, 30.0),
    (1800, 120, 32.0),
    (1000, 600, 1600 / 60)
])
def test_podcast_calc_duration(length, ad_seconds, expected):
    """ calc_duration returns the length incl. ads in minutes: (length + ad_seconds) / 60 """
    skip_if_incomplete(Podcast, ['length', 'ad_seconds'])
    podcast = Podcast('Echo der Zeit', length, 12, ad_seconds)
    skip_if_incomplete(Podcast, ['length', 'ad_seconds'], podcast)
    assert podcast.calc_duration() == pytest.approx(expected)


def test_podcast_subclass_of_medium():
    """ Podcast inherits from the abstract class Medium """
    assert issubclass(Podcast, Medium)
    assert 'calc_duration' in vars(Podcast)


def test_podcast_missing_arguments():
    """
    creating a Podcast without the required arguments raises a TypeError,
    but it works with all required arguments
    """
    assert Podcast('Echo der Zeit', 1800, 12) is not None
    with pytest.raises(TypeError):
        Podcast('Echo der Zeit', 1800)


def test_podcast_calc_ad_share():
    """ calc_ad_share returns the share of the advertisements in percent """
    skip_if_missing(Podcast, 'calc_ad_share')
    assert Podcast('Echo der Zeit', 1800, 12, 200).calc_ad_share() == pytest.approx(10.0)
    assert Podcast('Echo der Zeit', 1800, 12).calc_ad_share() == pytest.approx(0.0)
