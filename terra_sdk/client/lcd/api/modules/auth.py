import warnings
from typing import Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import AccAddress, Account, LazyGradedVestingAccount
from terra_sdk.error import AccountNotFoundWarning
from terra_sdk.util.validation import validate_acc_address

__all__ = ["account_info_type", "AuthApi"]
account_info_type = Union[Account, LazyGradedVestingAccount]


class AuthApi(BaseApi):
    def acc_info_for(
        self, address: AccAddress
    ) -> Union[ApiResponse, account_info_type]:
        address = validate_acc_address(address)
        info = self._api_get(f"/auth/accounts/{address}")
        if info["type"] == "core/Account":
            res = Account.from_data(info)
        elif info["type"] == "core/LazyGradedVestingAccount":
            res = LazyGradedVestingAccount.from_data(info)
        else:
            raise ValueError("could not deserialize account in auth.acc_info")
        if res.address is None:
            warnings.warn(
                "Account was not found; perhaps wrong chain or account needs to first be sent funds.",
                AccountNotFoundWarning,
            )
        return project(info, res)
