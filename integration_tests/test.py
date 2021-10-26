
def main():

    """
    import lcd_auth
    import lcd_authz
    import lcd_bank
    import lcd_distribution
    import lcd_gov
    import lcd_market
    import lcd_mint
    import lcd_oracle
    import lcd_slashing
    import lcd_wasm
    import lcd_treasury
    import lcd_tendermint
    import lcd_ibc
    import lcd_ibc_transfer
    """

    """
    TODO: pagination test
    import lcd_authz
    import lcd_bank
    import lcd_gov
    import lcd_slashing
    import lcd_staking
    import lcd_tx
    """

    import lcd_bank


    # stakin
    #result = terra.staking.delegations(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator=None)
    #result = terra.staking.delegations(validator=None, delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #result = terra.staking.delegations(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #result = terra.staking.delegation(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')

    # TODO: key not found only.. not tested for success case
    #result = terra.staking.unbonding_delegations(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #print('both', result)
    # TODO: untested
    #result = terra.staking.unbonding_delegations(validator='terravaloper1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs6gdt4x', delegator=None)
    #print('valonly', result)
    # TODO: untested
    #result = terra.staking.unbonding_delegations(validator=None, delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #print('delonly', result)
    # TODO: untested
    #result = terra.staking.unbonding_delegation(validator='terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef', delegator='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #print('single', result)
    """
    result = terra.staking.redelegations("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    print('redel with del', result)
    # TODO: valSRc, valDst test

    result = terra.staking.bonded_validators("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    print("bonded validators", result)

    result = terra.staking.validators()
    print("vals", result)

    result = terra.staking.validator("terravaloper1rdkyl03zd4d2g8hlchf0cmpwty2et4vfdjlaef")
    print("val", result)

    result = terra.staking.pool();
    print("pool", result)

    result = terra.staking.parameters();
    print("params", result)

    # tx - just querying APIs
    result = terra.tx.tx_info("")
    print("tx_info", result)
    result = terra.tx.txInfosByHeight()
    result = terra.tx.search()

    # tx - actual tx related
    result = terra.tx.encode()
    result = terra.tx.hash()

    result = terra.tx.estimate_fee()
    result = terra.tx.estimate_gas()
    result = terra.tx.compute_tax()
    result = terra.tx.create()

    # tx - broadcast
    result = terra.tx.broadcast()  # block-mode
    result = terra.tx.broadcast_sync()
    result = terra.tx.broadcast_async()

    # wallet related
    """

    #opt = PaginationOption(limit="1",count_total=True,offset=0)
    #print(f"[{str(opt)}]")

    #print(result)


main()
