from typing import List, Optional

from terra_sdk.core import AccAddress
from terra_sdk.core.msgauth import AuthorizationGrant

from ._base import BaseAPI


class MsgAuthAPI(BaseAPI):
    async def grants(
        self, granter: AccAddress, grantee: AccAddress, msg_type: Optional[str] = None
    ) -> List[AuthorizationGrant]:
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
