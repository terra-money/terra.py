from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from terra_sdk.core.sdk import Coins, Dec, PublicKey
from terra_sdk.util.serdes import terra_sdkBox, JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address

__all__ = ["Account", "VestingScheduleEntry", "LazyGradedVestingAccount"]


@dataclass
class Account(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^core/Account\Z"),
        value=S.OBJECT(
            address=S.ACC_ADDRESS,
            coins=Coins.__schema__,
            public_key=S.OPTIONAL(PublicKey.__schema__),
            account_number=S.STRING_INTEGER,
            sequence=S.STRING_INTEGER,
        ),
    )

    address: str
    coins: Coins
    public_key: Optional[PublicKey]
    account_number: int
    sequence: int

    def __post_init__(self):
        if self.address:
            self.address = validate_acc_address(self.address)
        if self.coins:
            self.coins = Coins(self.coins)
        self.account_number = int(self.account_number)
        self.sequence = int(self.sequence)

    def to_data(self) -> dict:
        d = dict(self.__dict__)
        d["account_number"] = str(self.account_number)
        d["sequence"] = str(self.sequence)
        return {"type": "core/Account", "value": d}

    @classmethod
    def from_data(cls, data: dict) -> Account:
        if "type" in data:
            data = data["value"]
        pk = data["public_key"]
        if pk is not None:
            pk = PublicKey.deserialize(data["public_key"])
        return cls(
            address=data["address"],
            coins=Coins.from_data(data["coins"]),
            public_key=pk,
            account_number=data["account_number"],
            sequence=data["sequence"],
        )


@dataclass
class VestingScheduleEntry(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        start_time=S.STRING_INTEGER, end_time=S.STRING_INTEGER, ratio=Dec.__schema__
    )

    start_time: int
    end_time: int
    ratio: Dec

    def to_data(self):
        return {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "ratio": self.ratio,
        }

    @classmethod
    def from_data(cls, data: dict) -> VestingScheduleEntry:
        return cls(
            start_time=int(data["start_time"]),
            end_time=int(data["end_time"]),
            ratio=Dec.from_data(data["ratio"]),
        )


@dataclass(init=False)
class LazyGradedVestingAccount(Account):

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^core/LazyGradedVestingAccount\Z"),
        value=S.OBJECT(
            BaseVestingAccount=S.OBJECT(
                BaseAccount=Account.__schema__["properties"]["value"],
                original_vesting=Coins.__schema__,
                delegated_free=Coins.__schema__,
                delegated_vesting=Coins.__schema__,
                end_time=S.STRING_INTEGER,
            ),
            vesting_schedules=S.ARRAY(
                S.OBJECT(
                    denom=S.STRING, schedules=S.ARRAY(VestingScheduleEntry.__schema__)
                )
            ),
        ),
    )

    original_vesting: Coins
    delegated_free: Coins
    delegated_vesting: Coins
    end_time: int
    vesting_schedules: Dict[str, List[VestingScheduleEntry]]

    def __init__(
        self,
        base_account: Account,
        original_vesting: Coins,
        delegated_free: Coins,
        delegated_vesting: Coins,
        end_time: int,
        vesting_schedules: Dict[str, List[VestingScheduleEntry]],
    ):
        Account.__init__(
            self,
            address=base_account.address,
            coins=base_account.coins,
            public_key=base_account.public_key,
            account_number=base_account.account_number,
            sequence=base_account.sequence,
        )
        self._base_account = base_account
        self.original_vesting = original_vesting
        self.delegated_free = delegated_free
        self.delegated_vesting = delegated_vesting
        self.end_time = end_time
        self.vesting_schedules = vesting_schedules

    def to_data(self):
        return {
            "type": "core/LazyGradedVestingAccount",
            "value": {
                "BaseVestingAccount": {
                    "BaseAccount": Account.to_data(self._base_account)["value"],
                    "original_vesting": self.original_vesting,
                    "delegated_free": self.delegated_free,
                    "delegated_vesting": self.delegated_vesting,
                    "end_time": str(self.end_time),
                },
                "vesting_schedules": [
                    {"denom": denom, "schedules": self.vesting_schedules[denom]}
                    for denom in self.vesting_schedules
                ],
            },
        }

    @property
    def pretty_data(self):
        d = dict(self.__dict__)
        d.pop("_base_account")
        return d.items()

    @classmethod
    def from_data(cls, data: dict) -> LazyGradedVestingAccount:
        if "type" in data:
            data = data["value"]  # disregard type
        bva = data[
            "BaseVestingAccount"
        ]  # value = { bva { ... } vesting_schedules { } }
        original_vesting = Coins.from_data(bva["original_vesting"])
        delegated_free = Coins.from_data(bva["delegated_free"])
        delegated_vesting = Coins.from_data(bva["delegated_vesting"])
        vesting_schedules = terra_sdkBox({})
        for s in data["vesting_schedules"]:
            vesting_schedules[s["denom"]] = [
                VestingScheduleEntry.deserialize(e) for e in s["schedules"]
            ]
        return cls(
            base_account=Account.from_data(bva["BaseAccount"]),
            original_vesting=original_vesting,
            delegated_free=delegated_free,
            delegated_vesting=delegated_vesting,
            end_time=int(bva["end_time"]),
            vesting_schedules=vesting_schedules,
        )
