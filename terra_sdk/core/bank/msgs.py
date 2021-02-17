"""Bank module message types."""

from __future__ import annotations

from typing import List

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import JSONSerializable

__all__ = ["MsgSend", "MsgMultiSend", "MultiSendIO"]

import attr


@attr.s
class MsgSend(Msg):
    """Sends native Terra assets (Luna or Terra stablecoins) from ``from_address`` to
    ``to_address``.

    Args:
        from_address: sender
        to_address: recipient
        amount (Coins): coins to send
    """

    type = "bank/MsgSend"
    """"""
    action = "send"
    """"""

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> MsgSend:
        data = data["value"]
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=Coins.from_data(data["amount"]),
        )


@attr.s
class MultiSendIO(JSONSerializable):
    """Organizes data for MsgMultiSend input/outputs. Expects data to be provided in the
    format:

    .. code-block:: python

        {
           "address": "terra1...",
           "coins": "123456789uusd"
        }
    """

    address: AccAddress = attr.ib()
    """Input / output address."""

    coins: Coins = attr.ib(converter=Coins)
    """Coins to be sent / received."""

    @classmethod
    def from_data(cls, data: dict):
        return cls(address=data["address"], coins=Coins.from_data(data["coins"]))


def convert_io_list(data: list) -> List[MultiSendIO]:
    if all(isinstance(x, MultiSendIO) for x in data):
        return data
    else:
        return [MultiSendIO(address=d["address"], coins=d["coins"]) for d in data]


@attr.s
class MsgMultiSend(Msg):
    """Allows batch-sending between multiple source and destination addresses.
    The total amount of coins in ``inputs`` must match ``outputs``. The transaction
    containing ``MsgMultiSend`` must contain signatures from all addresses used as inputs.

    The ``inputs`` and ``output`` arguments should be of the form:

    .. code-block:: python

        [{
            "address": "terra1...",
            "coins": "123456789uusd"
        },
        {
            "address": "terra12...",
            "coins": "2983298ukrw,21323uusd"
        }]


    Args:
        inputs (List[MultiSendIO]): senders and amounts
        outputs (List[MultiSendIO]): recipients and amounts
    """

    type = "bank/MsgMultiSend"
    """"""
    action = "multisend"
    """"""

    inputs: List[MultiSendIO] = attr.ib(converter=convert_io_list)
    outputs: List[MultiSendIO] = attr.ib(converter=convert_io_list)

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        data = data["value"]
        return cls(
            inputs=[MultiSendIO.from_data(x) for x in data["inputs"]],
            outputs=[MultiSendIO.from_data(x) for x in data["outputs"]],
        )
