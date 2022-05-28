# core msgs
from terra_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)
from terra_sdk.core.bank import MsgMultiSend, MsgSend
from terra_sdk.core.crisis import MsgVerifyInvariant
from terra_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
)
from terra_sdk.core.feegrant import MsgGrantAllowance, MsgRevokeAllowance
from terra_sdk.core.gov.msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from terra_sdk.core.ibc.msgs import (
    MsgAcknowledgement,
    MsgChannelCloseConfirm,
    MsgChannelCloseInit,
    MsgChannelOpenAck,
    MsgChannelOpenConfirm,
    MsgChannelOpenInit,
    MsgChannelOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgCreateClient,
    MsgRecvPacket,
    MsgSubmitMisbehaviour,
    MsgTimeout,
    MsgUpdateClient,
    MsgUpgradeClient,
)
from terra_sdk.core.ibc_transfer import MsgTransfer
from terra_sdk.core.slashing import MsgUnjail
from terra_sdk.core.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_sdk.core.wasm import (
    MsgClearAdmin,
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateAdmin,
)

from .base import create_demux, create_demux_proto, create_demux_unpack_any

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
authz_msgs = [
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
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
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
    MsgMigrateContract,
    MsgUpdateAdmin,
    MsgClearAdmin,
]
feegrant_msgs = [MsgGrantAllowance, MsgRevokeAllowance]

ibc_transfer_msgs = [MsgTransfer]
ibc_msgs = [
    MsgCreateClient,
    MsgUpdateClient,
    MsgUpgradeClient,
    MsgSubmitMisbehaviour,
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
    MsgChannelOpenInit,
    MsgChannelOpenTry,
    MsgChannelOpenAck,
    MsgChannelOpenConfirm,
    MsgChannelCloseInit,
    MsgChannelCloseConfirm,
    MsgRecvPacket,
    MsgTimeout,
    MsgAcknowledgement,
]
crisis_msgs = [MsgVerifyInvariant]

parse_msg = create_demux(
    [
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)

parse_proto = create_demux_proto(
    [
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)


parse_unpack_any = create_demux_unpack_any(
    [
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)
