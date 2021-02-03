from terra_sdk.core.bank import MsgMultiSend, MsgSend
from terra_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)
from terra_sdk.core.gov.msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from terra_sdk.core.market import MsgSwap, MsgSwapSend
from terra_sdk.core.msgauth import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)
from terra_sdk.core.oracle import (
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
    MsgExchangeRatePrevote,
    MsgExchangeRateVote,
)
from terra_sdk.core.slashing import MsgUnjail
from terra_sdk.core.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_sdk.core.wasm import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractOwner,
)

from .base import create_demux

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
market_msgs = [MsgSwap, MsgSwapSend]
msgauth_msgs = [
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
]
oracle_msgs = [
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
    MsgExchangeRatePrevote,
    MsgExchangeRateVote,
]
slashing_msgs = [MsgUnjail]
staking_msgs = [
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
]
wasm_msgs = [
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractOwner,
]

parse_msg = create_demux(
    [
        *bank_msgs,
        *distribution_msgs,
        *gov_msgs,
        *market_msgs,
        *oracle_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
    ]
)
