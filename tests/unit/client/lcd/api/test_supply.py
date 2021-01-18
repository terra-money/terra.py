import pytest

from testtools import LcdRequestTest


class TestSupplyApi:
    def test_supply_request(self, mock_terra):
        try:
            mock_terra.supply()
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/supply/total"
