from abc import ABC

from terra_sdk.util.json import JSONSerializable

from .base_account import BaseAccount
from .lazy_graded_vesting_account import LazyGradedVestingAccount


class Account(JSONSerializable):

    @classmethod
    def from_data(cls, data: dict):  # -> Account:
        if data['@type'] == BaseAccount.type_url:
            return BaseAccount.from_data(data)
        else:
            return LazyGradedVestingAccount.from_data(data)
