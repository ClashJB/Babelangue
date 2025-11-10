from bank import value

def test_rudebutrich():
    assert value("Good Morning") == 100
    assert value("Just another day right") == 100
    assert value("  34234FDEEk fdfrfda") == 100


def test_aight():
    assert value("Hi") == 20
    assert value("hi") == 20
    assert value("Hey") == 20
    assert value("hey") == 20

def test_niceandpoor():
    assert value("Hello") == 0
    assert value("hello") == 0
    assert value("hElLo") == 0
    assert value("HeLlO") == 0