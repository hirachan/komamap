from komamap.komamap import get_direction
import math

def test_1():
    p1 = (35.68347, 139.77429)
    p2 = (35.68357, 139.77429)
    expect = 0

    assert int(get_direction(p1, p2) + 0.5) == expect

def test_2():
    p1 = (35.68347, 139.77429)
    p2 = (35.68347, 139.77439)
    expect = 90

    assert int(get_direction(p1, p2) + 0.5) == expect

def test_3():
    p1 = (35.68347, 139.77429)
    p2 = (35.68337, 139.77429)
    expect = 180

    assert int(get_direction(p1, p2) + 0.5) == expect

def test_4():
    p1 = (35.68347, 139.77429)
    p2 = (35.68347, 139.77419)
    expect = 270

    assert int(get_direction(p1, p2) + 0.5) == expect
