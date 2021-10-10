from typing import Any
from boltons.iterutils import remap

__all__ = ["remove_none"]

dropper = lambda path, key, value: key is not None and value is not None


def remove_none(obj: dict):
    """remove keys for None in a dict"""
    return remap(obj, visit=dropper)
