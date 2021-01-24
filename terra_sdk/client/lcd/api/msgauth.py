from ._base import BaseAPI


class MsgAuthAPI(BaseAPI):
    async def grants(
        self, granter: str, grantee: str, msg_type: Optional[str] = None
    ) -> List[AuthorizationGrant]:
        if msg_type is None:
            res = await self._c._get(
                f"/msgauth/granters/{granter}/grantees/{grantee}/grants"
            )
            return list(map(AuthorizationGrant.from_data, res))
        else:
            res = await self._c._get(
                f"/msgauth/granters/{granter}/grantees/{grantee}/grants/{msgType}"
            )
            if res is None:
                return []
            else:
                return list(map(AuthorizationGrant.from_data, res))