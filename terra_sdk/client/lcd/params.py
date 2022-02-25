import abc
from abc import ABC
from typing import Optional

__all__ = ["APIParams", "PaginationOptions"]


class APIParams(ABC):
    @abc.abstractmethod
    def to_dict(self):
        pass

    def to_list(self) -> list:
        lst = []
        dct = self.to_dict()
        for key in dct.keys():
            lst.append((key, dct.get(key)))
        return lst


class PaginationOptions(APIParams):
    """This could be used when you need pagination options for APIs

    Args:
        key (str): key is a value returned in PageResponse.next_key to begin
            querying the next page most efficiently. Only one of offset or key
            should be set.
        offset (int): offset is a numeric offset that can be used when key is unavailable.
            It is less efficient than using key. Only one of offset or key should be set.
        limit (int): limit is the total number of results to be returned in the result page.
            If left empty it will default to a value to be set by each app.
        count_total (bool): count_total is set to true to indicate that the result set should include a count of
            the total number of items available for pagination in UIs.
            count_total is only respected when offset is used. It is ignored when key is set.
        reverse (bool): reverse is set to true if results are to be returned in the descending order.
    """

    def __init__(
        self,
        key: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        count_total: Optional[bool] = None,
        reverse: Optional[bool] = None,
    ):
        self.key = key
        self.offset = offset
        self.limit = limit
        self.count_total = count_total
        self.reverse = reverse

    def __str__(self):
        return "&".join(self.to_dict())

    def to_dict(self):
        params = {}
        if self.key is not None:
            params["pagination.key"] = self.key
        if self.offset is not None:
            params["pagination.offset"] = self.offset
        if self.limit is not None:
            params["pagination.limit"] = self.limit
        if self.count_total is not None:
            params["pagination.count_total"] = str(self.count_total).lower()
        if self.reverse is not None:
            params["pagination.reverse"] = str(self.reverse).lower()
        return params
