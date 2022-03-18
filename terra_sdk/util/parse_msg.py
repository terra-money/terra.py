from .base import create_demux, create_demux_proto

# core msgs
from terra_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)
from terra_sdk.core.bank import MsgMultiSend, MsgSend
from terra_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
)
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
from terra_sdk.core.market import MsgSwap, MsgSwapSend
from terra_sdk.core.oracle import (
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
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
    MsgClearContractAdmin,
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateCode,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractAdmin,
)
from terra_sdk.core.feegrant import (
    MsgGrantAllowance,
    MsgRevokeAllowance
)

# proto
from terra_proto.cosmos.authz.v1beta1 import MsgExec as MsgExec_pb
from terra_proto.cosmos.authz.v1beta1 import MsgGrant as MsgGrant_pb
from terra_proto.cosmos.authz.v1beta1 import MsgRevoke as MsgRevoke_pb
from terra_proto.cosmos.bank.v1beta1 import MsgMultiSend as MsgMultiSend_pb
from terra_proto.cosmos.bank.v1beta1 import MsgSend as MsgSend_pb
from terra_proto.cosmos.distribution.v1beta1 import (
    MsgFundCommunityPool as MsgFundCommunityPool_pb,
)
from terra_proto.cosmos.distribution.v1beta1 import (
    MsgSetWithdrawAddress as MsgSetWithdrawAddress_pb,
)
from terra_proto.cosmos.distribution.v1beta1 import (
    MsgWithdrawDelegatorReward as MsgWithdrawDelegatorReward_pb,
)
from terra_proto.cosmos.distribution.v1beta1 import (
    MsgWithdrawValidatorCommission as MsgWithdrawValidatorCommission_pb,
)
from terra_proto.cosmos.feegrant.v1beta1 import (
    MsgGrantAllowance as MsgGrantAllowance_pb,
)
from terra_proto.cosmos.feegrant.v1beta1 import (
    MsgRevokeAllowance as MsgRevokeAllowance_pb,
)
from terra_proto.cosmos.gov.v1beta1 import MsgDeposit as MsgDeposit_pb
from terra_proto.cosmos.gov.v1beta1 import MsgSubmitProposal as MsgSubmitProposal_pb
from terra_proto.cosmos.gov.v1beta1 import MsgVote as MsgVote_pb
from terra_proto.ibc.core.channel.v1 import MsgAcknowledgement as MsgAcknowledgement_pb
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelCloseConfirm as MsgChannelCloseConfirm_pb,
)
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelCloseInit as MsgChannelCloseInit_pb,
)
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenAck as MsgChannelOpenAck_pb
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelOpenConfirm as MsgChannelOpenConfirm_pb,
)
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenInit as MsgChannelOpenInit_pb
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenTry as MsgChannelOpenTry_pb
from terra_proto.ibc.core.channel.v1 import MsgRecvPacket as MsgRecvPacket_pb
from terra_proto.ibc.core.channel.v1 import MsgTimeout as MsgTimeout_pb
from terra_proto.ibc.core.client.v1 import MsgCreateClient as MsgCreateClient_pb
from terra_proto.ibc.core.client.v1 import (
    MsgSubmitMisbehaviour as MsgSubmitMisbehaviour_pb,
)
from terra_proto.ibc.core.client.v1 import MsgUpdateClient as MsgUpdateClient_pb
from terra_proto.ibc.core.client.v1 import MsgUpgradeClient as MsgUpgradeClient_pb
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenAck as MsgConnectionOpenAck_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenConfirm as MsgConnectionOpenConfirm_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenInit as MsgConnectionOpenInit_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenTry as MsgConnectionOpenTry_pb,
)
from terra_proto.ibc.applications.transfer.v1 import MsgTransfer as MsgTransfer_pb
from terra_proto.terra.market.v1beta1 import MsgSwap as MsgSwap_pb
from terra_proto.terra.market.v1beta1 import MsgSwapSend as MsgSwapSend_pb
from terra_proto.terra.oracle.v1beta1 import (
    MsgAggregateExchangeRatePrevote as MsgAggregateExchangeRatePrevote_pb,
)
from terra_proto.terra.oracle.v1beta1 import (
    MsgAggregateExchangeRateVote as MsgAggregateExchangeRateVote_pb,
)
from terra_proto.terra.oracle.v1beta1 import (
    MsgDelegateFeedConsent as MsgDelegateFeedConsent_pb,
)
from terra_proto.cosmos.slashing.v1beta1 import MsgUnjail as MsgUnjail_pb
from terra_proto.cosmos.staking.v1beta1 import (
    MsgBeginRedelegate as MsgBeginRedelegate_pb,
)
from terra_proto.cosmos.staking.v1beta1 import (
    MsgCreateValidator as MsgCreateValidator_pb,
)
from terra_proto.cosmos.staking.v1beta1 import MsgDelegate as MsgDelegate_pb
from terra_proto.cosmos.staking.v1beta1 import MsgEditValidator as MsgEditValidator_pb
from terra_proto.cosmos.staking.v1beta1 import MsgUndelegate as MsgUndelegate_pb
from terra_proto.terra.wasm.v1beta1 import (
    MsgClearContractAdmin as MsgClearContractAdmin_pb,
)
from terra_proto.terra.wasm.v1beta1 import MsgExecuteContract as MsgExecuteContract_pb
from terra_proto.terra.wasm.v1beta1 import (
    MsgInstantiateContract as MsgInstantiateContract_pb,
)
from terra_proto.terra.wasm.v1beta1 import MsgMigrateCode as MsgMigrateCode_pb
from terra_proto.terra.wasm.v1beta1 import MsgMigrateContract as MsgMigrateContract_pb
from terra_proto.terra.wasm.v1beta1 import MsgStoreCode as MsgStoreCode_pb
from terra_proto.terra.wasm.v1beta1 import (
    MsgUpdateContractAdmin as MsgUpdateContractAdmin_pb,
)

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
market_msgs = [MsgSwap, MsgSwapSend]
authz_msgs = [
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
]
oracle_msgs = [
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
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
    MsgMigrateCode,
    MsgInstantiateContract,
    MsgExecuteContract,
    MsgMigrateContract,
    MsgUpdateContractAdmin,
    MsgClearContractAdmin,
]
feegrant_msgs = [
    MsgGrantAllowance,
    MsgRevokeAllowance
]

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

parse_msg = create_demux(
    [
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *market_msgs,
        *oracle_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
    ]
)


bank_protos = [
    [MsgSend.type_url, MsgSend_pb],
    [MsgMultiSend.type_url, MsgMultiSend_pb]
]
distribution_protos = [
    [MsgFundCommunityPool.type_url, MsgFundCommunityPool_pb],
    [MsgSetWithdrawAddress.type_url, MsgSetWithdrawAddress_pb],
    [MsgWithdrawDelegatorReward.type_url, MsgWithdrawDelegatorReward_pb],
    [MsgWithdrawValidatorCommission.type_url, MsgWithdrawValidatorCommission_pb],
]
gov_protos = [
    [MsgDeposit.type_url, MsgDeposit_pb],
    [MsgSubmitProposal.type_url, MsgSubmitProposal_pb],
    [MsgVote.type_url, MsgVote_pb]
]
market_protos = [
    [MsgSwap.type_url, MsgSwap_pb],
    [MsgSwapSend.type_url, MsgSwapSend_pb]
]
authz_protos = [
    [MsgExecAuthorized.type_url, MsgExec_pb],
    [MsgGrantAuthorization.type_url, MsgGrant_pb],
    [MsgRevokeAuthorization.type_url, MsgRevoke_pb],
]
oracle_protos = [
    [MsgAggregateExchangeRatePrevote.type_url, MsgAggregateExchangeRatePrevote_pb],
    [MsgAggregateExchangeRateVote.type_url, MsgAggregateExchangeRateVote_pb],
    [MsgDelegateFeedConsent.type_url, MsgDelegateFeedConsent_pb],
]
slashing_protos = [
    [MsgUnjail.type_url, MsgUnjail_pb]
]
staking_protos = [
    [MsgBeginRedelegate.type_url, MsgBeginRedelegate_pb],
    [MsgCreateValidator.type_url, MsgCreateValidator_pb],
    [MsgDelegate.type_url, MsgDelegate_pb],
    [MsgEditValidator.type_url, MsgEditValidator_pb],
    [MsgUndelegate.type_url, MsgUndelegate_pb],
]
wasm_protos = [
    [MsgStoreCode.type_url, MsgStoreCode_pb],
    [MsgMigrateCode.type_url, MsgMigrateCode_pb],
    [MsgInstantiateContract.type_url, MsgInstantiateContract_pb],
    [MsgExecuteContract.type_url, MsgExecuteContract_pb],
    [MsgMigrateContract.type_url, MsgMigrateContract_pb],
    [MsgUpdateContractAdmin.type_url, MsgUpdateContractAdmin_pb],
    [MsgClearContractAdmin.type_url, MsgClearContractAdmin_pb],
]
feegrant_protos = [
    [MsgGrantAllowance.type_url, MsgGrantAllowance_pb],
    [MsgRevokeAllowance.type_url, MsgRevokeAllowance_pb]
]
ibc_transfer_protos = [
    [MsgTransfer.type_url, MsgTransfer_pb]
]
ibc_protos = [
    [MsgCreateClient.type_url, MsgCreateClient_pb],
    [MsgUpdateClient.type_url, MsgUpdateClient_pb],
    [MsgUpgradeClient.type_url, MsgUpgradeClient_pb],
    [MsgSubmitMisbehaviour.type_url, MsgSubmitMisbehaviour_pb],
    [MsgConnectionOpenInit.type_url, MsgConnectionOpenInit_pb],
    [MsgConnectionOpenTry.type_url, MsgConnectionOpenTry_pb],
    [MsgConnectionOpenAck.type_url, MsgConnectionOpenAck_pb],
    [MsgConnectionOpenConfirm.type_url, MsgConnectionOpenConfirm_pb],
    [MsgChannelOpenInit.type_url, MsgChannelOpenInit_pb],
    [MsgChannelOpenTry.type_url, MsgChannelOpenTry_pb],
    [MsgChannelOpenAck.type_url, MsgChannelOpenAck_pb],
    [MsgChannelOpenConfirm.type_url, MsgChannelOpenConfirm_pb],
    [MsgChannelCloseInit.type_url, MsgChannelCloseInit_pb],
    [MsgChannelCloseConfirm.type_url, MsgChannelCloseConfirm_pb],
    [MsgRecvPacket.type_url, MsgRecvPacket_pb],
    [MsgTimeout.type_url, MsgTimeout_pb],
    [MsgAcknowledgement.type_url, MsgAcknowledgement_pb],
]

parse_proto = create_demux_proto(
    [
        *authz_protos,
        *bank_protos,
        *distribution_protos,
        *feegrant_protos,
        *gov_protos,
        *market_protos,
        *oracle_protos,
        *slashing_protos,
        *staking_protos,
        *wasm_protos,
        *ibc_protos,
        *ibc_transfer_protos,
    ]
)
