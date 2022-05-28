from terra_sdk.core.feegrant import MsgGrantAllowance, MsgRevokeAllowance


def test_deserializes_msg_grant_allowance_examples():
    msg = {
          "@type": "/cosmos.feegrant.v1beta1.MsgGrantAllowance",
          "granter": "terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e",
          "grantee": "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
          "allowance": {
            "@type": "/cosmos.feegrant.v1beta1.BasicAllowance",
            "spend_limit": [
              {
                "denom": "uluna",
                "amount": "1000"
              }
            ],
            "expiration": "2050-01-01T00:00:00Z"
          }
    }
    print(MsgGrantAllowance.from_data(msg).to_data())

    assert MsgGrantAllowance.from_data(msg).to_data() == msg