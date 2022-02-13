from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    pagOpt = PaginationOptions(limit=1, count_total=True)

    # stakin
    # result = terra.staking.delegations(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator=None, params=pagOpt)
    # print("valonly", result)
    # result = terra.staking.delegations(validator=None, delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v', params=pagOpt)
    # print("delonly", result)
    # result = terra.staking.delegations(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    # print("both", result)
    # result = terra.staking.delegation(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    # print("single", result)

    # result = terra.staking.unbonding_delegations(validator='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', delegator='terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp')
    # print('both', result)
    # result = terra.staking.unbonding_delegations(validator='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', delegator=None)
    # print('valonly', result)
    # result = terra.staking.unbonding_delegations(validator=None, delegator='terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp', params=pagOpt)
    # print('delonly', result)
    # result = terra.staking.unbonding_delegation(validator='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', delegator='terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp')
    # print('single', result)

    # pagOpt = PaginationOptions(limit=3, count_total=True, reverse=False)
    # result = terra.staking.validators(pagOpt)
    # print("vals", result)

    # result = terra.staking.validator("terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef")
    # print("val", result)

    # pagOpt = PaginationOptions(limit=1, count_total=True, reverse=False)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", params=pagOpt)
    # print("all redels", result)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", validator_src='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', params=pagOpt)
    # print("src only", result)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", validator_dst='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', params=pagOpt)
    # print("dst only", result)
    # result = terra.staking.redelegations("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", validator_src='terravaloper1vk20anceu6h9s00d27pjlvslz3avetkvnwmr35', validator_dst='terravaloper1ze5dxzs4zcm60tg48m9unp8eh7maerma38dl84')
    # print("both", result)

    # result = terra.staking.bonded_validators("terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp", pagOpt)
    # print("bonded validators", result)

    # result = terra.staking.pool();
    # print("pool", result)

    # result = terra.staking.parameters();
    # print("params", result)


main()
