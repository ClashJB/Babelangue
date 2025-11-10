from fuel import convert, gauge

def test_convert():
    assert convert("3/4") == 75
    assert convert("4/4") == 100
    assert convert("0/4") == 0
    assert convert("2/0") == False

def test_gauge():
    assert gauge(100) == "F"
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(53) == "53%"
    assert gauge(101) == False
    assert gauge(-1) == False