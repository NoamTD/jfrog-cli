from .utils import normalize_host

def test_normalize_host():
    assert normalize_host("https://www.google.com") == "https://www.google.com"
    assert normalize_host("www.google.com") == "https://www.google.com"
    assert normalize_host("https://testhost.com/path?query=blabla") == "https://testhost.com"