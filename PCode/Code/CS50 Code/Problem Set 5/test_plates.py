from plates import is_valid

def test_charlimit():
    assert is_valid("A") == False
    assert is_valid("AB12345") == False
    assert is_valid("AB1234") == True

def test_twoletterstart():
    assert is_valid("A12345") == False
    assert is_valid("AB1234") == True
    assert is_valid("ABC123") == True

def test_nonumbersinbetween():
    assert is_valid("AB12CD") == False
    assert is_valid("ABCDEF") == True

def test_caseintensitivity():
    assert is_valid("aBcD12") == True
    assert is_valid("AbCdEf") == True