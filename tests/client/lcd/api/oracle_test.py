from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)


def test_exchange_rates():
    result = terra.oracle.exchange_rates()
    assert result is not None


def test_exchange_rate():
    result = terra.oracle.exchange_rate("ukrw")
    assert result is not None


def test_active_denoms():
    result = terra.oracle.active_denoms()
    assert result is not None


def test_feeder_address():
    result = terra.oracle.feeder_address(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    assert result is not None


def test_misses():
    result = terra.oracle.misses("terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw")
    assert result is not None


def test_aggregate_prevote():
    result = terra.oracle.aggregate_prevote(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    assert result is not None


# def test_aggregate_vote():
#    result = terra.oracle.aggregate_vote(
#        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
#    )
#    assert(result is not None)


def test_parameters():
    result = terra.oracle.parameters()
    assert result.get("vote_period")
    assert result.get("vote_threshold")
    assert result.get("reward_band")
    assert result.get("reward_distribution_window")
    assert result.get("whitelist")
    assert len(result.get("whitelist")) > 0
    assert result.get("slash_fraction")
    assert result.get("slash_window")
    assert result.get("min_valid_per_window")
