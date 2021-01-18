from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union

from terra_sdk.core import AccAddress, Coin, Coins
from terra_sdk.core.bank import Input, Output
from terra_sdk.core.msg import StdMsg
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address

__all__ = ["MsgSend", "MsgMultiSend"]


@dataclass
class MsgSend(StdMsg):

    type = "bank/MsgSend"
    action = "send"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^bank/MsgSend\Z"),
        value=S.OBJECT(
            from_address=S.ACC_ADDRESS,
            to_address=S.ACC_ADDRESS,
            amount=Coins.__schema__,
        ),
    )

    from_address: AccAddress
    to_address: AccAddress
    amount: Union[Coins, List[Coin]]

    def __post_init__(self):
        self.from_address = validate_acc_address(self.from_address)
        self.to_address = validate_acc_address(self.to_address)
        self.amount = Coins(self.amount)

    @classmethod
    def from_data(cls, data: dict) -> MsgSend:
        data = data["value"]
        amount = Coins.from_data(data["amount"])
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=amount,
        )


@dataclass(init=False)
class MsgMultiSend(StdMsg):

    type = "bank/MsgMultiSend"
    action = "multisend"

    Input = Input  # alias
    Output = Output  # alias

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^bank/MsgMultiSend\Z"),
        value=S.OBJECT(
            inputs=S.ARRAY(Input.__schema__), outputs=S.ARRAY(Output.__schema__)
        ),
    )

    inputs: List[Union[Input, dict]]
    outputs: List[Union[Output, dict]]

    def __init__(
        self, inputs: List[Input], outputs: List[Output],
    ):
        self.inputs = []
        self.outputs = []

        for i in inputs:
            if isinstance(i, dict):
                self.inputs.append(Input(address=i["address"], coins=i["coins"]))
            elif isinstance(i, Input):
                self.inputs.append(i)
            else:
                raise TypeError(
                    f"invalid item {type(i)} encountered in MsgMultiSend.inputs, can only accept 'Input' or 'dict'."
                )
        for o in outputs:
            if isinstance(o, dict):
                self.outputs.append(Output(address=o["address"], coins=o["coins"]))
            elif isinstance(o, Output):
                self.outputs.append(o)
            else:
                raise TypeError(
                    f"invalid item {type(o)} encountered in MsgMultiSend.outputs, can only accept 'Output' or 'dict'."
                )

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        data = data["value"]
        return cls(
            inputs=[Input.from_data(i) for i in data["inputs"]],
            outputs=[Output.from_data(o) for o in data["outputs"]],
        )
