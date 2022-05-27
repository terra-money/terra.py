from datetime import datetime


def to_isoformat(dt: datetime) -> str:
    return (
        dt.isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
        .replace(".000000Z", "Z")
    )
