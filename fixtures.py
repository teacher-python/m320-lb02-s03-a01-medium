""" Helpers for the pytests """
import pytest

from medium import Medium


class MediumDummy(Medium):
    """ concrete subclass, so the attributes of Medium can be tested """

    def calc_duration(self):
        """ dummy implementation of the abstract method """
        return 0.0


def skip_if_incomplete(cls, attrs, obj=None):
    """
    Skips the current test, if a property/setter or a private attribute is missing.
    :param cls: the class that must provide the properties with setters
    :param attrs: the names of the attributes (without underscore)
    :param obj: an object of the class to check the private attributes (optional)
    """
    missing = [attr for attr in attrs
               if not isinstance(getattr(cls, attr, None), property)
               or getattr(cls, attr).fset is None]
    if missing:
        pytest.skip(f'Test ignoriert, da in {cls.__name__} nicht alle Properties/Setter '
                    f'vorhanden sind (fehlend: {", ".join(missing)})')
    if obj is not None:
        missing = ['_' + attr for attr in attrs if '_' + attr not in vars(obj)]
        if missing:
            pytest.skip(f'Test ignoriert, da in {cls.__name__} nicht alle Attribute '
                        f'vorhanden sind (fehlend: {", ".join(missing)})')


def skip_if_missing(cls, name):
    """
    Skips the current test, if the class does not provide the method/property.
    :param cls: the class to check
    :param name: the name of the method or property
    """
    if name.startswith('__'):
        present = name in vars(cls)
    else:
        present = getattr(cls, name, None) is not None
    if not present:
        pytest.skip(f'Test ignoriert, da {name} in {cls.__name__} nicht vorhanden ist')
