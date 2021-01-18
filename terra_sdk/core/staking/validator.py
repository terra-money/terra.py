from __future__ import annotations

import attr

__all__ = [
    "CommissionRates",
    "Commission",
    "DoNotModifyDesc",
    "Description",
    "Validator",
]


@attr.s
class CommissionRates(JsonSerializable, JsonDeserializable):

    rate: Dec = attr.ib()
    max_rate: Dec = attr.ib()
    max_change_rate: Dec = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> CommissionRates:
        return cls(
            rate=Dec(data["rate"]),
            max_rate=Dec(data["max_rate"]),
            max_change_rate=Dec(data["max_change_rate"]),
        )


@attr.s
class Commission(JsonSerializable, JsonDeserializable):

    rates: CommissionRates = attr.ib()
    update_time: Timestamp = attr.ib()

    def to_data(self) -> Dict[str, Union[CommissionRates, Timestamp]]:
        return {"commission_rates": self.rates, "update_time": self.update_time}

    @classmethod
    def from_data(cls, data: dict) -> Commission:
        return cls(
            rates=CommissionRates.from_data(data["commission_rates"]),
            update_time=Timestamp.from_data(data["update_time"]),
        )


DoNotModifyDesc = "[do-not-modify]"  # from cosmos


@attr.s
class Description(JsonSerializable, JsonDeserializable):


    moniker: str = attr.ib()
    identity: str = attr.ib()
    website: str = attr.ib()
    details: str = attr.ib()

    @classmethod
    def do_not_modify(cls):
        return cls(DoNotModifyDesc, DoNotModifyDesc, DoNotModifyDesc, DoNotModifyDesc)

    @classmethod
    def from_data(cls, data) -> Description:
        return cls(data["moniker"], data["identity"], data["website"], data["details"])


@attr.s
class Validator(JsonSerializable, JsonDeserializable):



    operator_address: ValAddress = attr.ib()
    consensus_pubkey: str = attr.ib()
    jailed: bool = attr.ib()
    status_code: int = attr.ib()
    tokens: Coin = attr.ib()
    delegator_shares: Coin = attr.ib()
    description: Description = attr.ib()
    unbonding_height: int = attr.ib()
    unbonding_time: Timestamp = attr.ib()
    commission: Commission = attr.ib()
    min_self_delegation: int = attr.ib()

    @property
    def status(self) -> str:
        """String version of `status_code`"""
        return ["unbonded", "unbonding", "bonded"][self.status_code]

    def to_data(self) -> dict:
        s = self
        d = dict(self.__dict__)
        del d["status_code"]
        d["status"] = s.status_code
        d["tokens"] = str(s.tokens.amount)
        d["delegator_shares"] = str(s.delegator_shares.amount)
        d["unbonding_height"] = str(s.unbonding_height)
        d["min_self_delegation"] = str(s.min_self_delegation)
        return d

    @classmethod
    def from_data(cls, data: dict) -> Validator:
        return cls(
            operator_address=data["operator_address"],
            consensus_pubkey=data["consensus_pubkey"],
            jailed=data["jailed"],
            status_code=data["status"],
            tokens=Coin(uLuna, data["tokens"]),
            delegator_shares=Coin(uLuna, data["delegator_shares"]),
            description=Description.from_data(data["description"]),
            unbonding_height=int(data["unbonding_height"]),
            unbonding_time=Timestamp.from_data(data["unbonding_time"]),
            commission=Commission.from_data(data["commission"]),
            min_self_delegation=int(data["min_self_delegation"]),
        )
