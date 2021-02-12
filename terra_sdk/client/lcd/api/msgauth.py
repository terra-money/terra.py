from typing import List, Optional

from terra_sdk.core import AccAddress
from terra_sdk.core.msgauth import AuthorizationGrant

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncMsgAuthAPI", "MsgAuthAPI"]


class AsyncMsgAuthAPI(BaseAsyncAPI):
    async def grants(
        self, granter: AccAddress, grantee: AccAddress, msg_type: Optional[str] = None
    ) -> List[AuthorizationGrant]:
        """Fetches current active message authorization grants.

        Args:
            granter (AccAddress): granter account address
            grantee (AccAddress): grantee account address
            msg_type (Optional[str], optional): message type.

        Returns:
            List[AuthorizationGrant]: message authorization grants matching criteria
        """
        if msg_type is None:
            res = await self._c._get(
                f"/msgauth/granters/{granter}/grantees/{grantee}/grants"
            )
            return [AuthorizationGrant.from_data(x) for x in res]
        else:
            res = await self._c._get(
                f"/msgauth/granters/{granter}/grantees/{grantee}/grants/{msg_type}"
            )
            if res is None:
                return []
            else:
                return [AuthorizationGrant.from_data(x) for x in res]


class MsgAuthAPI(AsyncMsgAuthAPI):
    @sync_bind(AsyncMsgAuthAPI.grants)
    def grants(
        self, granter: AccAddress, grantee: AccAddress, msg_type: Optional[str] = None
    ) -> List[AuthorizationGrant]:
        pass

    grants.__doc__ = AsyncMsgAuthAPI.grants.__doc__
