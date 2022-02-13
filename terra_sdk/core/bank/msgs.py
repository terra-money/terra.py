"""Bank module message types."""

from __future__ import annotations

from typing import Any, List

from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.bank.v1beta1 import Input as Input_pb
from terra_proto.cosmos.bank.v1beta1 import MsgMultiSend as MsgMultiSend_pb
from terra_proto.cosmos.bank.v1beta1 import MsgSend as MsgSend_pb
from terra_proto.cosmos.bank.v1beta1 import Output as Output_pb

from terra_sdk.core import AccAddress, Coin, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import JSONSerializable

__all__ = ["MsgSend", "MsgMultiSend", "MultiSendInput", "MultiSendOutput"]

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

    type_amino = "bank/MsgSend"
    """"""
    type_url = "/cosmos.bank.v1beta1.MsgSend"
    """"""
    action = "send"
    """"""

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "amount": self.amount.to_amino()
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSend:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=Coins.from_data(data["amount"]),
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount.to_data(),
        }

    @classmethod
    def from_proto(cls, proto: MsgSend_pb) -> MsgSend:
        return cls(
            from_address=proto["from_address"],
            to_address=proto["to_address"],
            amount=Coins.from_proto(proto["amount"]),
        )

    def to_proto(self) -> MsgSend_pb:
        proto = MsgSend_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.amount = [c.to_proto() for c in self.amount]
        return proto

    @classmethod
    def unpack_any(cls, any: Any) -> MsgSend:
        return MsgSend.from_proto(any)


@attr.s
class MultiSendInput(JSONSerializable):
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

    def to_amino(self) -> dict:
        return {
            "address": self.address,
            "coins": self.coins.to_amino()
        }

    def to_data(self) -> dict:
        return {"address": self.address, "coins": self.coins.to_data()}

    @classmethod
    def from_data(cls, data: dict):
        return cls(address=data["address"], coins=Coins.from_data(data["coins"]))

    @classmethod
    def from_proto(cls, proto: Input_pb) -> MultiSendInput:
        return cls(address=proto["address"], coins=Coins.from_proto(proto["coins"]))

    def to_proto(self) -> Input_pb:
        proto = Input_pb()
        proto.address = self.address
        proto.coins = self.coins.to_proto()
        return proto


@attr.s
class MultiSendOutput(JSONSerializable):
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

    def to_amino(self) -> dict:
        return {
            "address": self.address,
            "coins": self.coins.to_amino()
        }

    @classmethod
    def from_data(cls, data: dict):
        return cls(address=data["address"], coins=Coins.from_data(data["coins"]))

    def to_data(self) -> dict:
        return {"address": self.address, "coins": self.coins.to_data()}

    @classmethod
    def from_proto(cls, proto: Output_pb) -> MultiSendOutput:
        return cls(address=proto["address"], coins=Coins.from_proto(proto["coins"]))

    def to_proto(self) -> Output_pb:
        proto = Output_pb()
        proto.address = self.address
        proto.coins = self.coins.to_proto()
        return proto


def convert_input_list(data: list) -> List[MultiSendInput]:
    if all(isinstance(x, MultiSendInput) for x in data):
        return data
    else:
        return [MultiSendInput(address=d["address"], coins=d["coins"]) for d in data]


def convert_output_list(data: list) -> List[MultiSendOutput]:
    if all(isinstance(x, MultiSendOutput) for x in data):
        return data
    else:
        return [MultiSendOutput(address=d["address"], coins=d["coins"]) for d in data]


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

    type_amino = "bank/MsgMultiSend"
    """"""
    type_url = "/cosmos.bank.v1beta1.MsgMultiSend"
    """"""
    action = "multisend"
    """"""

    inputs: List[MultiSendInput] = attr.ib(converter=convert_input_list)
    outputs: List[MultiSendOutput] = attr.ib(converter=convert_output_list)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "inputs": [mi.to_amino() for mi in self.inputs],
                "outputs": [mo.to_amino() for mo in self.inputs],
            }
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "inputs": [mi.to_data() for mi in self.inputs],
            "outputs": [mo.to_data() for mo in self.outputs],
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        return cls(
            inputs=[MultiSendInput.from_data(x) for x in data["inputs"]],
            outputs=[MultiSendOutput.from_data(x) for x in data["outputs"]],
        )

    @classmethod
    def from_proto(cls, proto: MsgMultiSend_pb) -> MsgMultiSend:
        return cls(
            inputs=[MultiSendInput.from_proto(x) for x in proto["inputs"]],
            outputs=[MultiSendOutput.from_proto(x) for x in proto["outputs"]],
        )

    def to_proto(self) -> MsgMultiSend_pb:
        return MsgMultiSend_pb(
            inputs=[i.to_proto() for i in self.inputs],
            outputs=[o.to_proto() for o in self.outputs],
        )
