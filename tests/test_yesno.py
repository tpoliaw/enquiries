from answers import yesno

def test_keys():
    assert yesno.keys('y', 'n', True) == ' [Y/n]'
