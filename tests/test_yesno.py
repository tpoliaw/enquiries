from answers import yesno

def test_keys():
    assert yesno._keys('y', 'n', True) == ' [Y/n]'
    assert yesno._keys('y', 'n', False) == ' [y/N]'
