import furl

def urljoin(base: str, url: str) -> str:
    return furl.furl(base).add(path=url).url

