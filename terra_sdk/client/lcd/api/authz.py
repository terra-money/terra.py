from typing import List, Optional

from terra_sdk.core import AccAddress
from terra_sdk.core.authz import AuthorizationGrant

from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncAuthzAPI", "AuthzAPI"]

from ..params import PaginationOptions


class AsyncAuthzAPI(BaseAsyncAPI):
    async def grants(
        self,
        granter: AccAddress,
        grantee: AccAddress,
        msg_type: Optional[str] = None,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        """Fetches current active message authorization grants.

        Args:
            granter (AccAddress): granter account address
            grantee (AccAddress): grantee account address
            msg_type (Optional[str], optional): message type.

        Returns:
            List[AuthorizationGrant]: message authorization grants matching criteria
        """
        params = {
            "granter": granter,
            "grantee": grantee,
        }
        if msg_type is not None:
            params["msg_type_url"] = msg_type

        res = await self._c._get(f"/cosmos/authz/v1beta1/grants", params)
        return [AuthorizationGrant.from_data(x) for x in res["grants"]]


class AuthzAPI(AsyncAuthzAPI):
    @sync_bind(AsyncAuthzAPI.grants)
    def grants(
        self,
        granter: AccAddress,
        grantee: AccAddress,
        msg_type: Optional[str] = None,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        pass

    grants.__doc__ = AsyncAuthzAPI.grants.__doc__
