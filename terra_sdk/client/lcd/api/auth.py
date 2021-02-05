from typing import Union

from terra_sdk.core import AccAddress
from terra_sdk.core.auth import Account, LazyGradedVestingAccount

from ._base import BaseAPI


class AuthAPI(BaseAPI):
    async def account_info(
        self, address: AccAddress
    ) -> Union[Account, LazyGradedVestingAccount]:
        result = await self._c._get(f"/auth/accounts/{address}")
        if result["type"] == "core/Account":
            return Account.from_data(result)
        else:
            return LazyGradedVestingAccount.from_data(result)
