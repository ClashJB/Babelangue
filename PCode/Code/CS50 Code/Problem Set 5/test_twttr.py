from twttr import shorten

def test_shorten():
    assert shorten("Gugu Gaga File python crap") == "Gg Gg Fl pythn crp"
    assert shorten("I am happy   ") == "m hppy"
    assert shorten(" Just setting up my twitter. ") == "Jst sttng p my twttr."