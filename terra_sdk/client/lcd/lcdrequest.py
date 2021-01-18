import attr

__all__ = ["LcdRequest"]

import attr

@attr.s
class LcdRequest:
    method: str = attr.ib()
    url: str = attr.ib()
    kwargs: dict = attr.ib()
