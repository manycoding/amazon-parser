import requests


def do_get(url):
    """Wrapper for HTTP GET. Returns None if request failed"""
    r = requests.get(url)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(str(e))
        return None
    return r
