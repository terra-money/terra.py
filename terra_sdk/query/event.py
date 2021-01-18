from collections import defaultdict
from typing import Dict, Iterable, List

from toolz import valmap

from terra_sdk.core.event import Event
from terra_sdk.util.pretty import PrettyPrintable
from terra_sdk.util.serdes import terra_sdkBox

__all__ = ["EventsQuery"]


class EventsQuery(PrettyPrintable):
    """Convenience query structure around a list of events.

    events[n] (n = int) --> n-th event
    events["event-type"] --> list of events of that type
    events.event_type --> list of events of that type
    for e in events: --> iterate over events
    "send" in events: --> whether events of this type are in collection
    """

    def __init__(self, events: Iterable[Event]):
        self.events = list(events)
        by_type = defaultdict(list)  # TODO: remove double representation..
        for e in self.events:
            by_type[e.type].append(e)
        self.by_type: terra_sdkBox[str, List[Event]] = terra_sdkBox(by_type)

    def __repr__(self) -> str:
        r = ", ".join(f"{t}: {n}" for t, n in self.types.items())
        if r == "":
            r = "(empty)"
        return f"<EventsQuery {r}>"

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.events[key]
        elif isinstance(key, slice):
            return EventsQuery(self.events[key])
        elif isinstance(key, str):
            # TODO: refactor by the example of MsgInfosQuery
            if key in self.by_type:
                return EventsQuery(self.by_type[key])
            else:
                return EventsQuery([])
        else:
            raise KeyError(
                f"unusable key {key} for EventsQuery, use 'int', 'slice', or 'str'"
            )

    def __getattr__(self, name):
        return self[name]

    def __len__(self) -> int:
        return sum(map(len, self.by_type.values()))

    def __iter__(self):
        return iter(self.events)

    @property
    def types(self) -> Dict[str, int]:
        return valmap(len, self.by_type)

    def __contains__(self, item):
        return item in self.by_type

    def to_dict(self) -> dict:  # for printing
        return self.by_type.to_dict()

    @property
    def pretty_data(self):
        return self.types.items()
