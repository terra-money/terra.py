from dataclasses import dataclass

__all__ = ["LcdRequest"]


@dataclass
class LcdRequest:
    method: str
    url: str
    kwargs: dict
