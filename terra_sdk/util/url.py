import furl

def urljoin(base: str, url: str) -> str:
    return furl.furl(base.removesuffix('/')).add(path=url).url

