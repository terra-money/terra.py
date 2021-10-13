from furl import furl  # type: ignore


def urljoin(base: str, url: str) -> str:
    return furl(base.rstrip("/")).add(path=url).url
