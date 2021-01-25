from __future__ import annotations

from .distribution.msgs import *
from .gov.msgs import *
from .market.msgs import *
from .msgauth.msgs import *
from .oracle.msgs import *
from .slashing.msgs import *
from .staking.msgs import *
from .treasury.msgs import *
from .wasm.msgs import *


class Msg:
    @staticmethod
    def from_data(data: dict) -> Msg:
        pass
