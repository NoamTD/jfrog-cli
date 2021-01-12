from urllib import parse
from urllib.parse import urlparse

def normalize_host(url: str):
    parsed_url = urlparse(url, scheme="https")
    
    if parsed_url.netloc != '' and parsed_url.netloc != None:
        host = parsed_url.netloc
    elif parsed_url.hostname != '' and parsed_url.hostname is not None:
        host = parsed_url.hostname
    else:
        host = parsed_url.path.split('/')[0]
    
    result = f'{parsed_url.scheme}://{host}'

    return result
