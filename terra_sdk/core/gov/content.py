import attr

from terra_sdk.util.base import BaseTerraData


@attr.s
class Content(BaseTerraData):

    title: str = attr.ib()
    description: str = attr.ib()
