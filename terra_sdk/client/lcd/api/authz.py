from typing import List, Optional

from terra_sdk.core import AccAddress
from terra_sdk.core.authz import AuthorizationGrant

from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncAuthzAPI", "AuthzAPI"]


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
            msg_type (str, optional): message type.
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[AuthorizationGrant]: message authorization grants matching criteria
        """
        params = {
            "granter": granter,
            "grantee": grantee,
        }
        if msg_type is not None:
            params["msg_type_url"] = msg_type

        res = await self._c._get("/cosmos/authz/v1beta1/grants", params)
        return [AuthorizationGrant.from_data(x) for x in res["grants"]]

    async def granter(
        self,
        granter: AccAddress,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        """Fetches list of `GrantAuthorization` granted by granter.

        Args:
            granter (AccAddress): granter account address
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[AuthorizationGrant]: message authorization grants matching criteria
        """

        res = await self._c._get(
            f"/cosmos/authz/v1beta1/grants/granter/{granter}", params
        )
        return [AuthorizationGrant.from_data(x) for x in res["grants"]]

    async def grantee(
        self,
        grantee: AccAddress,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        """Fetches list of `GrantAuthorization` by grantee.

        Args:
            grantee (AccAddress): grantee account address
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[AuthorizationGrant]: message authorization grants matching criteria
        """

        res = await self._c._get(
            f"/cosmos/authz/v1beta1/grants/grantee/{grantee}", params
        )
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

    @sync_bind(AsyncAuthzAPI.granter)
    def granter(
        self,
        granter: AccAddress,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        pass

    @sync_bind(AsyncAuthzAPI.grantee)
    def grantee(
        self,
        grantee: AccAddress,
        params: Optional[APIParams] = None,
    ) -> List[AuthorizationGrant]:
        pass

    grants.__doc__ = AsyncAuthzAPI.grants.__doc__
    granter.__doc__ = AsyncAuthzAPI.granter.__doc__
    grantee.__doc__ = AsyncAuthzAPI.grantee.__doc__
