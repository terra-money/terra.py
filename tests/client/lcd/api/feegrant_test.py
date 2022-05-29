from terra_sdk.client.lcd import LCDClient, PaginationOptions

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)


pagOpt = PaginationOptions(limit=2, count_total=True)


def test_allowances():
    result, _ = terra.feegrant.allowances(
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp"
    )
    assert result is not None
    assert len(result) >= 0


def test_allowance():
    result = terra.feegrant.allowance(
        "terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e",
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
    )

    assert result is not None
    assert result["granter"] == "terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e"
    assert result["grantee"] == "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp"
