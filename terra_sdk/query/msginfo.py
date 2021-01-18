import json
from typing import Dict, Iterable, List

import wrapt
from toolz import groupby, valmap

from terra_sdk.core import StdMsg
from terra_sdk.query.event import EventsQuery
from terra_sdk.util.pretty import PrettyPrintable, see
from terra_sdk.util.serdes import terra_sdkBox
from terra_sdk.util.validation import Schemas as S

__all__ = ["MsgInfo", "MsgInfosQuery"]


class MsgInfo(wrapt.ObjectProxy):

    __schema__ = S.OBJECT(
        msg_index=S.INTEGER,
        success=S.BOOLEAN,
        log=S.STRING,
        events=S.ARRAY(
            S.OBJECT(
                type=S.STRING,
                attributes=S.ARRAY(S.OBJECT(key=S.STRING, value=S.STRING)),
            )
        ),
    )

    def __init__(self, msg: StdMsg, success: bool, log: dict, events: EventsQuery):
        wrapt.ObjectProxy.__init__(self, msg)
        try:
            log = json.loads(log)
            if type(log) == dict:
                log = terra_sdkBox(log)
        except:
            log = None
        self._self_success = success
        self._self_log = log
        self._self_events = events
        self._self_pretty_data = None

    @property
    def success(self):
        return self._self_success

    @property
    def log(self):
        return self._self_log

    @property
    def events(self):
        return self._self_events

    def __eq__(self, other):
        return (
            isinstance(other, MsgInfo)
            and self.success == other.success
            and self.log == other.log
            and self.events == other.events
        )

    def __ne__(self, other):
        # we have to do this because objectproxy uses the underlying wrapped's __neq__
        return not self == other

    @property
    def pretty_data(self):
        d = dict(self.__dict__)
        items = list(d.items())
        items.append(("success", self.success))
        if self.log:
            items.append(("log", self.log))
        items.append(("events", self.events))
        return items

    def _pretty_output(self, path: str = ""):
        return PrettyPrintable._pretty_output(self, path)

    def _pretty_repr_(self, path: str = "") -> str:
        return PrettyPrintable._pretty_repr_(self, path)

    @property
    def _pp(self):
        """Shortcut for seeing pretty-printing output."""
        see(self)
        return None


class MsgInfosQuery(PrettyPrintable):
    """Convenience query structure around a list of MsgInfo objects.

    Use the variable name "msgs" if possible.

    msgs[n] (n = int) --> n-th MsgInfo
    msgs["msg-type / msg-action"] --> recursive query of MsgInfos of that type / action
    msgs.msg_action --> list of msginfos of that action
    for e in msgs: --> iterate over msginfos
    "send" in msgs: --> whether msgs of this action are in collection
    """

    def __init__(self, msginfos: Iterable[MsgInfo]):
        self.msginfos = list(msginfos)

    def __repr__(self) -> str:
        r = ", ".join(f"{t}: {n}" for t, n in self.actions.items())
        if r == "":
            r = "(empty)"
        return f"<MsgInfosQuery {r}>"

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.msginfos[key]
        if isinstance(key, slice):
            return MsgInfosQuery(self.msginfos[key])
        elif isinstance(key, str):
            return MsgInfosQuery(
                [m for m in self.msginfos if m.type == key or m.action == key]
            )
        elif hasattr(key, "type") and hasattr(key, "action"):
            return MsgInfosQuery(
                [
                    m
                    for m in self.msginfos
                    if m.type == key.type and m.action == key.action
                ]
            )
        else:
            return self.msginfos[key]

    def __getattr__(self, name):
        return self[name]

    def __iter__(self):
        return iter(self.msginfos)

    def __contains__(self, item):
        if isinstance(item, StdMsg):
            return item.type in self.types
        else:
            return item in self.types or self.actions

    @property
    def logs(self) -> List[terra_sdkBox]:
        msg_logs = [m.log for m in self.msginfos if m.log is not None]
        return msg_logs

    @property
    def events(self) -> EventsQuery:
        msg_events = [event for m in self.msginfos for event in m.events]
        return EventsQuery(msg_events)

    @property
    def types(self) -> Dict[str, int]:
        msg_types = groupby(lambda m: m.type, self.msginfos)
        msg_types = valmap(len, msg_types)
        return msg_types

    @property
    def actions(self) -> Dict[str, int]:
        msg_actions = groupby(lambda m: m.action, self.msginfos)
        msg_actions = valmap(len, msg_actions)
        return msg_actions

    def __len__(self) -> int:
        return len(self.msginfos)

    # TODO: add printing mechanism?
    # Example:
    # a = terra_sdkBox({ x: MsgInfo(...) })
    # print(a)

    @property
    def pretty_data(self):
        items = groupby(lambda m: str(m.__class__.__name__), self.msginfos)
        items = valmap(len, items)
        return items.items()
