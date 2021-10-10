from boltons.iterutils import remap  # type: ignore

__all__ = ["remove_none"]


def remove_none(obj: dict):
    """remove keys for None in a dict"""
    return remap(
        obj, visit=lambda path, key, value: key is not None and value is not None
    )
