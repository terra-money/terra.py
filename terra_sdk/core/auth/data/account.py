from abc import ABC, abstractmethod

from terra_sdk.util.json import JSONSerializable

from .base_account import BaseAccount
from .lazy_graded_vesting_account import LazyGradedVestingAccount
from terra_sdk.core.public_key import PublicKey


class Account(JSONSerializable):

    @abstractmethod
    def get_sequence(self) -> int:
        pass

    @abstractmethod
    def get_public_key(self) -> PublicKey:
        pass

    @classmethod
    def from_data(cls, data: dict):  # -> Account:
        if data['@type'] == BaseAccount.type_url:
            return BaseAccount.from_data(data)
        else:
            return LazyGradedVestingAccount.from_data(data)
