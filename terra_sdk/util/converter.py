from datetime import datetime


def to_isoformat(dt: datetime) -> str:
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z").replace("000Z", "Z")


def replace_bytes_index(text: bytes, index = 0, replacement: bytes = ''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])
