from datetime import datetime

import pytest
from hypothesis import assume, given
from hypothesis_jsonschema import from_schema

from terra_sdk.core.sdk.timestamp import Timestamp
from testtools import assert_serdes_consistent, assert_serdes_exact


@pytest.mark.sdk
class TestTimestampSerdes:

    # TODO: write better regex so it is consistent.
    # @pytest.mark.serdes
    # @given(m=from_schema(Timestamp.__schema__))
    # def test_serdes_consistent(self, m):
    #     assert_serdes_consistent(Timestamp, m)

    def test_frac_second(self):
        examples = [
            "2019-04-24T06:05:20Z",
            "2019-04-24T06:05:10Z",
            "2019-06-02T22:23:38.000400591Z",
            "2020-02-24T03:48:05.950000000Z",
            "2020-02-07T12:41:42.636901000Z",
            "2020-02-22T01:05:40.237804060Z",
            "2020-02-04T13:26:16.364509600Z",
        ]
        for x in examples:
            ts = Timestamp.deserialize(x).to_data()
            assert ts == x

    def test_frac_second_ns_precision(self):
        examples = [
            (
                "2019-04-24T06:05:20.123456789123456789Z",
                "2019-04-24T06:05:20.123456789Z",
            ),
            ("2019-04-24T06:05:20.12Z", "2019-04-24T06:05:20.12Z",),
            ("2019-04-24T06:05:20.12345Z", "2019-04-24T06:05:20.12345Z",),
        ]
        for x in examples:
            ts = Timestamp.deserialize(x[0]).to_data()
            assert ts == x[1]

    def test_from_datetime(self):
        dt = datetime.now()
        ts = Timestamp.from_datetime(dt)
        dt_format = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        ts_format = str(ts)
        assert dt_format == ts_format
        assert dt == ts

    def test_cmp(self):
        ts0 = Timestamp(2004, 12, 18, 19, 54, 22, 333333000, 9)
        ts1 = Timestamp(2004, 12, 18, 19, 54, 22, 333333333, 9)
        ts2 = Timestamp(2004, 12, 18, 19, 54, 22, 333333999, 9)
        ts3 = Timestamp(2004, 12, 18, 19, 54, 22, 533333999, 9)
        dt = datetime(2004, 12, 18, 19, 54, 22, 333333)
        dt2 = datetime(2004, 12, 18, 19, 54, 22, 433333)

        assert dt == ts0
        assert dt != ts1
        assert dt != ts2

        assert ts0 != ts1
        assert ts0 != ts2
        assert ts1 != ts2

        assert ts0 < ts1
        assert ts1 < ts2
        assert ts2 < dt2

        assert ts2 > dt
        assert ts1 > dt
        assert ts2 > ts1

        assert dt2 > ts2
        assert dt < ts3

        in_order = [dt, ts0, ts1, ts2, dt2, ts3]
        assert sorted([ts3, dt2, ts0, dt, ts1, ts2]) == in_order
