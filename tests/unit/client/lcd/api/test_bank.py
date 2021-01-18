import pytest

from terra_sdk.error import InvalidAccAddress
from testtools import LcdRequestTest


class TestBankApi:
    def test_balance_for_request(self, mock_terra, acc_address, val_address):
        address = acc_address
        try:
            mock_terra.bank.balance_for(address)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/bank/balances/{address}"

        with pytest.raises(InvalidAccAddress):
            mock_terra.bank.balance_for(val_address)
