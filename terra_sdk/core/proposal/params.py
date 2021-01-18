from __future__ import annotations

import json
import re
import attr, field

from bidict import bidict

from terra_sdk.core.proposal import Content
from terra_sdk.core.sdk import Coins, Dec
from terra_sdk.core.treasury import PolicyConstraints
from terra_sdk.error import InvalidParamChange
from terra_sdk.util.serdes import (
    terra_sdkBox,
    JsonDeserializable,
    JsonSerializable,
    serialize_to_json,
)
from terra_sdk.util.validation import Schemas as S

__all__ = ["ParamChanges", "ParameterChangeProposal"]

symbol = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$")

ParamChangeSchema = S.OBJECT(subspace=S.STRING, key=S.STRING, value=S.STRING)

# For each subspace, map JSON-param key to (ParamStore key, deserializing-fn, serialiazing-fn)
# Serializing function is necessary due to weird ways Cosmos's params module treats integers.

# TODO: This file could use some work.

# Define the deserialization and serialization functions for governance params
def deserialize_deposit(data: dict):
    if data.get("min_deposit"):
        data["min_deposit"] = Coins.deserialize(data["min_deposit"])
    if data.get("max_deposit_period"):
        data["max_deposit_period"] = int(data["max_deposit_period"])
    return data


def serialize_deposit(data: dict):
    if data.get("max_deposit_period"):
        data["max_deposit_period"] = str(int(data["max_deposit_period"]))
    return data


def deserialize_voting(data: dict):
    if data.get("voting_period"):
        data["voting_period"] = int(data["voting_period"])
    return data


def serialize_voting(data: dict):
    if data.get("voting_period"):
        data["voting_period"] = str(int(data["voting_period"]))
    return data


def deserialize_tally(data: dict):
    if data.get("quorum"):
        data["quorum"] = Dec(data["quorum"])
    if data.get("threshold"):
        data["threshold"] = Dec(data["threshold"])
    if data.get("veto"):
        data["veto"] = Dec(data["veto"])
    return data


def serialize_tally(data: dict):
    return data


# TODO: this could be refactored into XXXModuleParams class in core, with keys
# as attributes, and API requests for Module Params give you an instance of
# ModuleParams with all keys loaded with their current values. Then, to build
# param changes, you would instantiate an empty ModuleParams class with the
# values initialized to ModuleParams.EMPTY and then set each one.

PARAM_DEFNS = {
    "distribution": {
        "community_tax": ("communitytax", Dec),
        "base_proposer_reward": ("baseproposerreward", Dec),
        "bonus_proposer_reward": ("bonusproposerreward", Dec),
        "withdraw_addr_enabled": ("withdrawaddrenabled", bool),
    },
    "staking": {
        "unbonding_time": ("UnbondingTime", int, str),
        "max_validators": ("MaxValidators", int, int),
        "max_entries": ("KeyMaxEntries", int, int),
        "bond_denom": ("BondDenom", str),
    },
    "slashing": {
        "max_evidence_age": ("MaxEvidenceAge", int, str),  # no longer in cosmos master/
        "signed_blocks_window": ("SignedBlocksWindow", int, str),
        "min_signed_per_window": ("MinSignedPerWindow", Dec),
        "downtime_jail_duration": ("DowntimeJailDuration", int, str),
        "slash_fraction_double_sign": ("SlashFractionDoubleSign", Dec),
        "slash_fraction_downtime": ("SlashFractionDowntime", Dec),
    },
    "oracle": {
        "vote_period": ("voteperiod", int, str),
        "vote_threshold": ("votethreshold", Dec),
        "reward_band": ("rewardband", Dec),
        "reward_distribution_window": ("rewarddistributionwindow", int, str),
        "whitelist": ("whitelist", None),
        "slash_fraction": ("slashfraction", Dec),
        "slash_window": ("slashwindow", int, str),
        "min_valid_per_window": ("minvalidperwindow", Dec),
    },
    "market": {
        "pool_recovery_period": ("poolrecoveryperiod", int, str),
        "base_pool": ("basepool", Dec),
        "min_spread": ("minspread", Dec),
        "illiquid_tobin_tax_list": ("illiquidtobintaxlist", None),
    },
    "treasury": {
        "tax_policy": ("taxpolicy", PolicyConstraints.deserialize),
        "reward_policy": ("rewardpolicy", PolicyConstraints.deserialize),
        "min_spread": ("minspread", Dec),
        "seigniorage_burden_target": ("seigniorageburdentarget", Dec),
        "mining_increment": ("miningincrement", Dec),
        "window_short": ("windowshort", int, str),
        "window_long": ("windowlong", int, str),
        "window_probation": ("windowprobation", int, str),
    },
    "gov": {
        "deposit_params": ("depositparams", deserialize_deposit, serialize_deposit),
        "voting_params": ("votingparams", deserialize_voting, serialize_voting),
        "tally_params": ("tallyparams", deserialize_tally, serialize_tally),
    },
}

# create lookup table for deserialization
DES_LOOKUP_TABLE = {}
for subspace, keys in PARAM_DEFNS.items():
    DES_LOOKUP_TABLE[subspace] = {d[0]: d[1] for k, d in keys.items()}

# DES_LOOKUP_TABLE[subspace][paramkey aka d[0]] = JSON param key
# DES_LOOKUP_TABLE["treasury"]["windowlong"] -> "window_long"

# create lookup table for serialization
PARAMSTORE_KEY_LOOKUP_TABLE = {}
for subspace, keys in PARAM_DEFNS.items():
    PARAMSTORE_KEY_LOOKUP_TABLE[subspace] = bidict({k: d[0] for k, d in keys.items()})


class ParamChanges(JsonSerializable, JsonDeserializable):

    def __init__(self, changes: dict):
        for k, v in changes.items():
            m = symbol.match(k)
            if not m:
                raise InvalidParamChange(
                    f"Parameter change subspace could not be parsed: {k}"
                )
            if not isinstance(v, dict):
                raise InvalidParamChange(
                    f"Parameter change value should be a dict but got: '{type(v)}' for {k}"
                )
            for sk, sv in v.items():
                sm = symbol.match(sk)
                if not sm:
                    raise InvalidParamChange(
                        f"Parameter change key could not be parsed - {k}: '{sk}'"
                    )
        self.changes = terra_sdkBox(changes)

    def __repr__(self) -> str:
        return f"<ParamChanges {self.changes!r}>"

    def __getattr__(self, name: str) -> terra_sdkBox:
        return self.changes[name]

    def __getitem__(self, item) -> terra_sdkBox:
        return self.changes[item]

    @staticmethod
    def _get_key(subspace, key, inverse=False):
        """Each parameter has a special key in the ParamStore that might not correspond
        to the parameter's JSON-name. We use this function to look up the ParamStore key
        for the JSON-name, which we are familiar with.

        Set `inverse` to `True` to look up from the opposite direction for deserialization.
        """
        try:
            table = PARAMSTORE_KEY_LOOKUP_TABLE[subspace]
            if inverse:
                table = table.inverse
            return table[key]
        except KeyError:
            return key

    @staticmethod
    def _marshal_value(subspace, key, value):
        """Formats the value for param change. Terra node expects all the values to be
        JSON-encoded, and Amino:JSON int/int64/uint/uint64 expects quoted values for
        JavaScript numeric support, and int16/uint16 need `int`.
        """
        try:
            if key not in PARAM_DEFNS[subspace]:  # if not JSON-name
                # try paramstore name
                key = ParamChanges._get_key(subspace, key, inverse=True)
            if len(PARAM_DEFNS[subspace][key]) == 3:
                value = PARAM_DEFNS[subspace][key][2](value)
        except KeyError:
            pass
        return serialize_to_json(value)

    @staticmethod
    def _unmarshal_value(subspace, key, value):
        """Looks up the correct type to decode the right type for the parameter change."""
        if subspace in DES_LOOKUP_TABLE and key in DES_LOOKUP_TABLE[subspace]:
            if DES_LOOKUP_TABLE[subspace][key] is not None:
                return DES_LOOKUP_TABLE[subspace][key](value)
        return value

    def to_data(self) -> list:
        param_changes = []
        for subspace, v in self.changes.items():
            for key, value in v.items():
                param_changes.append(
                    {
                        "subspace": subspace,
                        "key": self._get_key(subspace, key),
                        "value": self._marshal_value(subspace, key, value),
                    }
                )
        return param_changes

    @classmethod
    def from_data(cls, data: list) -> ParamChanges:
        changes = terra_sdkBox(default_box=True)
        for p in data:
            subspace = p["subspace"]
            key = cls._get_key(
                subspace, p["key"], inverse=True
            )  # p["key"] is paramstore key, we are using json-name keys inside terra_sdk
            value = cls._unmarshal_value(subspace, p["key"], json.loads(p["value"]))
            changes[subspace][key] = value
        return cls(changes)


@attr.s
class ParameterChangeProposal(Content):

    type = "params/ParameterChangeProposal"
    ParamChanges = ParamChanges  # alias for easy access

    title: str                     = attr.ib()
    description: str               = attr.ib()
    changes: ParamChanges  = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            changes=ParamChanges.from_data(data["changes"]),
        )
