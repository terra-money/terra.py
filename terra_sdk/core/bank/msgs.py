"""Bank module message types."""

from __future__ import annotations

from typing import List

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg

__all__ = ["MsgSend", "MsgMultiSend"]

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
class MsgMultiSend(Msg):
    """Allows batch-sending between multiple source and destination addresses.
    The total amount of coins in ``inputs`` must match ``outputs``. The transaction
    containing ``MsgMultiSend`` must contain signatures from all addresses used as inputs.

    The ``inputs`` and ``output`` arguments should be of the form::

        [{
            "address": "terra1...",
            "amount": "123456789"
        },
        {
            "address": "terra12...",
            "amount": "2983298"
        }]

    And so forth..

    Args:
        inputs: senders
        outputs: recipients
    """

    type = "bank/MsgMultiSend"
    """"""
    action = "multisend"
    """"""

    # TODO: improve interface - match terra.js
    inputs: List[dict] = attr.ib()
    outputs: List[dict] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        data = data["value"]
        return cls(
            inputs=data["inputs"],
            outputs=data["outputs"],
        )
