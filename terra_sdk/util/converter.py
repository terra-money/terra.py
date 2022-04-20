from datetime import datetime


def to_isoformat(dt: datetime) -> str:
    return (
        dt.isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
        .replace(".000Z", "Z")
    )
