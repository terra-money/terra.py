from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

pagOpt = PaginationOptions(limit=1, count_total=True)


def test_delegations():
    result = terra.staking.delegations(
        validator="terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef",
        delegator=None,
        params=pagOpt,
    )
    assert result is not None
    result = terra.staking.delegations(
        validator=None,
        delegator="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        params=pagOpt,
    )
    assert result is not None
    result = terra.staking.delegations(
        validator="terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef",
        delegator="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
    )
    assert result is not None
    result = terra.staking.delegation(
        validator="terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef",
        delegator="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
    )
    assert result is not None


def test_unbonding():
    # result = terra.staking.unbonding_delegations(validator='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35',
    #                                              delegator='terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp')
    # assert(result is not None)
    result = terra.staking.unbonding_delegations(
        validator="terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35", delegator=None
    )
    assert result is not None
    result = terra.staking.unbonding_delegations(
        validator=None,
        delegator="terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
        params=pagOpt,
    )
    assert result is not None
    # result = terra.staking.unbonding_delegation(validator='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35',
    #                                             delegator='terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp')
    # assert(result is not None)


def test_validators():
    _pagOpt = PaginationOptions(limit=3, count_total=True, reverse=False)
    result = terra.staking.validators(_pagOpt)
    assert result is not None
    result = terra.staking.validator(
        "terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef"
    )
    assert result is not None


def test_redelagations():
    _pagOpt = PaginationOptions(limit=1, count_total=True, reverse=False)
    result = terra.staking.redelegations(
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", params=_pagOpt
    )
    assert result is not None
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
    #                                      validator_src='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35',
    #                                      params=_pagOpt)
    # assert(result is not None)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
    #                                      validator_dst='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35',
    #                                      params=_pagOpt)
    # assert(result is not None)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
    #                                      validator_src='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35',
    #                                      validator_dst='terravaloper1ze5dxzs4zcm60tg48m9unp8eh7maerma38dl84')
    # assert(result is not None)


def test_bonded_validators():
    result = terra.staking.bonded_validators(
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", pagOpt
    )
    assert result is not None


def test_pool():
    result = terra.staking.pool()
    assert result is not None


def test_parameters():
    result = terra.staking.parameters()
    assert result.get("unbonding_time")
    assert result.get("max_validators")
    assert result.get("max_entries")
    assert result.get("historical_entries")
    assert result.get("bond_denom")
