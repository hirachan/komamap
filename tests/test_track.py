from komamap.track import Track, Point


def test_1():
    t = Track()
    p1 = Point(0, 0)
    t.append(p1)

    assert t[0] is p1


def test_2():
    t = Track()
    p1 = Point(0, 0)
    t.append(p1)

    p2 = Point(0, 0)
    t.append(p2)

    assert t[0].next is p2
    assert t[1].prev is p1
