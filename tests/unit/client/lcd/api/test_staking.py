import pytest

from testtools import LcdRequestTest


class TestStakingApi:
    def test_delegations_request(self, mock_terra, acc_address, val_address):
        acc = acc_address
        val = val_address
        with pytest.raises(TypeError):
            mock_terra.staking.delegations()
        with pytest.raises(TypeError):
            mock_terra.staking.delegation(delegator=acc)
        with pytest.raises(TypeError):
            mock_terra.staking.delegation(validator=val)
        try:
            mock_terra.staking.delegations(delegator=acc)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/delegators/{acc}/delegations"
        try:
            mock_terra.staking.delegations(validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/validators/{val}/delegations"
        try:
            mock_terra.staking.delegations(delegator=acc, validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/delegators/{acc}/delegations/{val}"
        try:
            mock_terra.staking.delegation(delegator=acc, validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/delegators/{acc}/delegations/{val}"

    def test_unbonding_delegations_request(self, mock_terra, acc_address, val_address):
        acc = acc_address
        val = val_address

        with pytest.raises(TypeError):
            mock_terra.staking.unbonding_delegations()
        with pytest.raises(TypeError):
            mock_terra.staking.unbonding_delegation(delegator=acc)
        with pytest.raises(TypeError):
            mock_terra.staking.unbonding_delegation(validator=val)

        try:
            mock_terra.staking.unbonding_delegations(delegator=acc)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/delegators/{acc}/unbonding_delegations"
        try:
            mock_terra.staking.unbonding_delegations(validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert request.url == f"/staking/validators/{val}/unbonding_delegations"
        try:
            mock_terra.staking.unbonding_delegations(delegator=acc, validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert (
                request.url == f"/staking/delegators/{acc}/unbonding_delegations/{val}"
            )
        try:
            mock_terra.staking.unbonding_delegation(delegator=acc, validator=val)
        except LcdRequestTest as request:
            assert request.method == "get"
            assert (
                request.url == f"/staking/delegators/{acc}/unbonding_delegations/{val}"
            )

    def test_redelegations_request(self, mock_terra, acc_address, make_val_address):
        acc = acc_address
        val1 = make_val_address()
        val2 = make_val_address()

        try:
            mock_terra.staking.redelegations()
        except LcdRequestTest as r:
            assert r.method == "get"
            assert r.url == "/staking/redelegations"
            assert r.kwargs["params"] == {}

        try:
            mock_terra.staking.redelegations(acc, val1, val2)
        except LcdRequestTest as r:
            assert r.method == "get"
            assert r.url == "/staking/redelegations"
            p = r.kwargs["params"]
            assert p["delegator"] == acc
            assert p["validator_from"] == val1
            assert p["validator_to"] == val2

    def test_bonded_validators_for(self, mock_terra, acc_address, val_address):
        acc = acc_address
        try:
            mock_terra.staking.bonded_validators_for(acc)
        except LcdRequestTest as r:
            assert r.method == "get"
            assert r.url == f"/staking/delegators/{acc}/validators"
