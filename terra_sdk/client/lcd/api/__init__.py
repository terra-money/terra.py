from __future__ import annotations

from typing import Any, Optional, Union

import requests
import wrapt

from terra_sdk.error import UnhandledResponse

__all__ = ["ApiResponse", "BaseApi", "project"]


class ApiResponse(wrapt.ObjectProxy):
    """Wraps the LCD API response in an object proxy that keeps track of the chain height
    reported at the time of the request, as well as the orginal requests.Response (which
    includes the request) object. This lets users use the parsed response directly, as
    well as keep potentitally useful information."""

    def __init__(
        self, result: Any, response: requests.Response, height: Optional[int] = None
    ):
        wrapt.ObjectProxy.__init__(self, result)
        self._self_result = result
        self._self_response = response
        self._self_height = height

    def __repr__(self):
        return f"<ApiResponse {self.__wrapped__!r}>"

    @property
    def __type__(self):
        return type(self._self_result)

    @property
    def __result__(self) -> Any:
        """Unwraps the APIResponse to get the underlying wrapped object."""
        return self._self_result

    @property
    def __request__(self) -> requests.Request:
        """The `requests.Requests` object used for the request."""
        return self._self_response.request

    @property
    def __response__(self) -> requests.Response:
        """The original `requests.Response` object."""
        return self._self_response

    @property
    def __height__(self) -> int:
        """Chain height reported at the response (may be `None` for some queries)."""
        return self._self_height


def project(a: ApiResponse, b: Any) -> Union[ApiResponse, Any]:
    """Creates a new `ApiResponse` out of `b` by projecting `a`'s response and height
    metadata."""
    # we don't want russian dolls of ApiResponses
    while isinstance(b, ApiResponse):
        b = b.__result__  # unpack
    return ApiResponse(b, a.__response__, a.__height__)


class BaseApi(object):
    """Base class for Terra API objects. Provides functions for turning an API response
    into a wrapped object proxy called an `ApiResponse`."""

    def __init__(self, terra):
        self.terra = terra

    @property
    def lcd(self):
        return self.terra.lcd

    def _api_get(self, path, unwrap=True, **kwargs) -> Union[ApiResponse, Any]:
        return self._handle_response(self.terra.lcd.get(path, **kwargs), unwrap)

    def _api_post(self, path, unwrap=True, **kwargs) -> Union[ApiResponse, Any]:
        return self._handle_response(self.terra.lcd.post(path, **kwargs), unwrap)

    @staticmethod
    def _handle_response(
        response: requests.Response, unwrap=True
    ) -> Union[ApiResponse, Any]:
        """Creates an ApiResponse object from the LCD Client's response.

        :param response: LCD response
        :param unwrap: whether the LCD response will include height
        """
        # TODO: refactor into middleware? --
        # NOTE: This actually should be in the last step, but the user can decide to do
        # some post-processing on their own, such as parsing, by writing a library that
        # parses the result. Outside the scope of the SDK.
        try:
            res = response.json()
            if unwrap:
                return ApiResponse(res["result"], response, int(res["height"]))
            else:
                return ApiResponse(res, response, None)
        except ValueError:  # if the response cannot be parsed to JSON
            raise UnhandledResponse(f"unhandled response {str(response.content)}")
