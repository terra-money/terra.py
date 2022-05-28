from abc import ABC, abstractmethod

from terra_sdk.core.public_key import PublicKey
from terra_sdk.util.json import JSONSerializable

from .base_account import BaseAccount
from .continuous_vesting_account import ContinuousVestingAccount
from .delayed_vesting_account import DelayedVestingAccount
from .periodic_vesting_account import PeriodicVestingAccount


class Account(JSONSerializable, ABC):
    @abstractmethod
    def get_account_number(self) -> int:
        pass

    @abstractmethod
    def get_sequence(self) -> int:
        pass

    @abstractmethod
    def get_public_key(self) -> PublicKey:
        pass

    @classmethod
    def from_amino(cls, amino: dict):  # -> Account:
        if amino["type"] == BaseAccount.type_amino:
            return BaseAccount.from_amino(amino)
        elif amino["type"] == ContinuousVestingAccount.type_amino:
            return ContinuousVestingAccount.from_amino(amino)
        elif amino["type"] == DelayedVestingAccount.type_amino:
            return DelayedVestingAccount.from_amino(amino)
        elif amino["type"] == PeriodicVestingAccount.type_amino:
            return PeriodicVestingAccount.from_amino(amino)

    @classmethod
    def from_data(cls, data: dict):  # -> Account:
        if data["@type"] == BaseAccount.type_url:
            return BaseAccount.from_data(data)
        elif data["@type"] == ContinuousVestingAccount.type_url:
            return ContinuousVestingAccount.from_data(data)
        elif data["@type"] == DelayedVestingAccount.type_url:
            return DelayedVestingAccount.from_data(data)
        elif data["@type"] == PeriodicVestingAccount.type_url:
            return PeriodicVestingAccount.from_data(data)
