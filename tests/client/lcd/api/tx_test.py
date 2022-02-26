from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)

pagOpt = PaginationOptions(limit=2, count_total=True)


def test_tx_info():
    result = terra.tx.tx_info(
        "7AB5550F54A1B6B8A480C6B870DFFB1E94D6DB7579F9620E4172525476B8BBA2"
    )
    assert result is not None


def test_search():
    result = terra.tx.search(
        [
            ("tx.height", 7549440),
            ("message.sender", "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"),
        ]
    )
    assert result is not None
    assert len(result) > 0


def test_tx_infos_by_height():
    result = terra.tx.tx_infos_by_height()
    assert result is not None


def test_tx_infos_by_height_with_height():
    result = terra.tx.tx_infos_by_height(7549440)
    assert result is not None
