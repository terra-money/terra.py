from __future__ import annotations

import concurrent.futures
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List
from urllib.parse import urljoin

import requests
from requests_futures.sessions import FuturesSession

from terra_sdk.__version__ import __version__

from .lcdrequest import LcdRequest
from .middlewares import (
    handle_codespace_errors,
    handle_general_errors,
    set_query,
    set_timeout,
)

pv = sys.version_info

CLIENT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": f"terra_sdk v{__version__} (Python {pv[0]}.{pv[1]}.{pv[2]})",
}


def create_session():
    session = requests.session()
    session.headers.update(CLIENT_HEADERS)
    return session


class LcdClient(object):
    """Manages the connection to a Terra LCD node, helps with procesing requests."""

    def __init__(self, terra, url: str = "", timeout: int = 30, threads: int = 1):
        self.url = url
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=self._nthreads)
        self.session = create_session()

    @property
    def threads(self) -> int:
        return self._nthreads

    @threads.setter
    def threads(self, other: int):
        self._nthreads = other
        self.executor = ThreadPoolExecutor(max_workers=self._nthreads)

    def _create_url(self, path):
        return urljoin(self.url, path)

    def _build_request(self, method, path, kwargs):
        """Applies middlewares to request."""
        request = LcdRequest(method=method, url=self._create_url(path), kwargs=kwargs)
        for req_m in self.request_middlewares:
            request = req_m(self, request)  # TODO: use reduce()
        return request

    def _send_request(self, request, use_future=False):
        session = self.futures_session if use_future else self.session
        return getattr(session, request.method)(request.url, **request.kwargs)

    def handle_response(self, response):
        """Applies middlewares to response."""
        r = response
        for resp_m in self.response_middlewares:
            r = resp_m(self, r)
        return r

    def _request(self, method, path, **kwargs):
        request = self._build_request(method, path, kwargs)
        response = self._send_request(request)
        return self.handle_response(response)

    def get(self, path, build=False, **kwargs):
        if build:  # builds a GET request, but does not send.
            return self._build_request("get", path, kwargs)
        return self._request("get", path, **kwargs)

    def post(self, path, build=False, **kwargs):
        if build:
            return self._build_request("post", path, kwargs)
        return self._request("post", path, **kwargs)
