from .base_api import BaseAPI


class AuthAPI(BaseAPI):
    async def account_info(self, address: str) -> None:
        result = await self._c.get(f"/auth/accounts/{address}")
        if result["type"] == "core/Account":
            return Account.from_data(result)
        else:
            return LazyGradedVestingAccount.from_data(result)