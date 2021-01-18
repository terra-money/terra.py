from typing import List, Optional, Set, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import (
    AccAddress,
    Coin,
    Coins,
    Dec,
    ExchangeRatePrevote,
    ExchangeRateVote,
    ValAddress
)
from terra_sdk.error import DenomNotFound
from terra_sdk.util.serdes import terra_sdkBox
from terra_sdk.util.validation import validate_val_address

__all__ = ["OracleApi"]


class OracleApi(BaseApi):

    # for some reason, votes and prevotes for a certain (val, denom) pair will give STILL give you a list
    def votes(
        self, validator: Optional[ValAddress] = None, denom: Optional[str] = None
    ) -> Union[ApiResponse, List[ExchangeRateVote]]:
        if validator is not None and denom is not None:
            validator = validate_val_address(validator)
            res = self._api_get(f"/oracle/denoms/{denom}/votes/{validator}")
        elif validator:
            validator = validate_val_address(validator)
            res = self._api_get(f"/oracle/voters/{validator}/votes")
        elif denom:
            res = self._api_get(f"/oracle/denoms/{denom}/votes")
        else:
            raise ValueError("arguments validator and denom cannot both be None")
        return project(res, [ExchangeRateVote.deserialize(vote) for vote in res])

    def prevotes(
        self, validator: Optional[ValAddress] = None, denom: Optional[str] = None
    ) -> Union[ApiResponse, List[ExchangeRatePrevote]]:
        if validator is not None and denom is not None:
            validator = validate_val_address(validator)
            res = self._api_get(f"/oracle/denoms/{denom}/prevotes/{validator}")
        elif validator:
            validator = validate_val_address(validator)
            res = self._api_get(f"/oracle/voters/{validator}/prevotes")
        elif denom:
            res = self._api_get(f"/oracle/denoms/{denom}/prevotes")
        else:
            raise ValueError("arguments validator and denom cannot both be None")
        return project(
            res, [ExchangeRatePrevote.deserialize(prevote) for prevote in res]
        )

    def exchange_rates(self) -> Union[ApiResponse, Coins]:
        """Gets all exchange rates."""
        res = self._api_get("/oracle/denoms/exchange_rates")
        return project(res, Coins.from_data(res))

    def exchange_rate(self, denom: str) -> Union[ApiResponse, Coin]:
        """Gets the exchange rate of LUNA against one denomination."""
        res = self.exchange_rates()
        if denom not in res:
            raise DenomNotFound(
                f"denom '{denom}' not found, available denoms: {res.denoms}"
            )
        return project(res, res[denom])

    def active_denoms(self) -> Union[ApiResponse, Set[str]]:
        res = self._api_get("/oracle/denoms/actives")
        return project(res, set(res))

    def feeder_address_for(
        self, validator: ValAddress
    ) -> Union[ApiResponse, AccAddress]:
        validator = validate_val_address(validator)
        return self._api_get(f"/oracle/voters/{validator}/feeder")

    def misses_for(self, validator: ValAddress) -> Union[ApiResponse, int]:
        validator = validate_val_address(validator)
        res = self._api_get(f"/oracle/voters/{validator}/miss")
        return project(res, int(res))

    def params(
        self, key: Optional[str] = None
    ) -> Union[ApiResponse, dict, int, Dec, List[str]]:
        res = self._api_get("/oracle/parameters")
        p = terra_sdkBox(
            res,
            box_recast={
                "vote_period": int,
                "vote_threshold": Dec,
                "reward_band": Dec,
                "reward_distribution_window": int,
                "slash_fraction": Dec,
                "slash_window": int,
                "min_valid_per_window": Dec,
            },
        )
        return project(res, p[key] if key else p)
