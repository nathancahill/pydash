
import time
import pydash as pyd

from . import fixtures
from .fixtures import parametrize


def test_now():
    assert pyd.now() == int(time.time() * 1000)


@parametrize('case', [
    'foo',
    'bar'
])
def test_constant(case):
    assert pyd.constant(case)() == case


@parametrize('case,expected', [
    ((1,), 1),
    ((1, 2), 1),
    ((), None)
])
def test_identity(case, expected):
    assert pyd.identity(*case) == expected


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred',   'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
])
def test_property_(case, arg, expected):
    getter = pyd.property_(case)
    assert pyd.map_(arg, getter) == expected


@parametrize('case', [
    pyd.prop
])
def test_property_aliases(case):
    assert pyd.property_ is case


@parametrize('case,minimum,maximum', [
    ((), 0, 1),
    ((25,), 0, 25),
    ((5, 10), 5, 10)
])
def test_random(case, minimum, maximum):
    for _ in range(50):
        assert minimum <= pyd.random(*case) <= maximum


@parametrize('case,floating,minimum,maximum', [
    ((), True, 0, 1),
    ((25,), True, 0, 25),
    ((5, 10), True, 5, 10),
    ((5.0, 10), False, 5, 10),
    ((5, 10.0), False, 5, 10),
    ((5.0, 10.0), False, 5, 10),
    ((5.0, 10.0), True, 5, 10),
])
def test_random_float(case, floating, minimum, maximum):
    for _ in range(50):
        rnd = pyd.random(*case, floating=floating)
        assert isinstance(rnd, float)
        assert minimum <= rnd <= maximum


@parametrize('case,expected', [
    ((), None),
    ((1, 2, 3), None)
])
def test_noop(case, expected):
    assert pyd.noop(*case) == expected
