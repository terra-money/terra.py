from unittest import mock

import asynctest
from aioresponses import aioresponses

from terra_sdk.client.lcd import LCDClient


class TestDoSessionGet(asynctest.TestCase):
    @aioresponses()
    def test_makes_request_to_expected_url(self, mocked):
        mocked.get(
            "https://lcd.terra.dev/node_info", status=200, body='{"response": "test"}'
        )
        terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")

        resp = terra.tendermint.node_info()

        assert resp == {"response": "test"}

    @aioresponses()
    def test_does_not_strip_access_token(self, mocked):
        mocked.get(
            "https://lcd.terra.dev/access_token/node_info",
            status=200,
            body='{"response": "test"}',
        )
        terra = LCDClient(
            chain_id="columbus-5", url="https://lcd.terra.dev/access_token/"
        )

        resp = terra.tendermint.node_info()

        assert resp == {"response": "test"}


if __name__ == "__main__":
    asynctest.main()
