import attr

@attr.s
class StdFee(JsonSerializable, JsonDeserializable):

    gas: int = 0
    amount: Coins = field(default_factory=Coins)

    def to_data(self) -> dict:
        return {"gas": str(self.gas), "amount": self.amount}

    @property
    def min_gas_prices(self) -> Coins:
        return self.amount.dec_coins / self.gas

    @classmethod
    def make(cls, gas: int = 0, **denoms):
        amount = Coins()
        for denom in denoms:
            amount += Coin(denom, denoms[denom])
        return cls(gas=gas, amount=amount)

    @classmethod
    def from_data(cls, data: dict) -> StdFee:
        return cls(gas=int(data["gas"]), amount=Coins.from_data(data["amount"]))