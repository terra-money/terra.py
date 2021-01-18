import pytest

from terra_sdk.error import InvalidAccAddress
from testtools import LcdRequestTest


class TestAuthApi:
    def test_acc_address_for_request(self, mock_terra, acc_address, val_address):
        address = acc_address
        try:
            mock_terra.auth.acc_info_for(address)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/auth/accounts/{address}"

        with pytest.raises(InvalidAccAddress):
            mock_terra.auth.acc_info_for(val_address)
