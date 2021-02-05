from terra_sdk.core.strings import AccAddress, AccPubKey, ValAddress, ValPubKey


def test_validates_account_address():
    assert not AccAddress.validate(
        "terravaloper1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0yhqtk"
    )
    assert not AccAddress.validate(
        "terra1pdx498r0h7c2fj36sjhs8vu8rz9hd2cw0tmam9"
    )  # bad checksum
    assert not AccAddress.validate("cosmos176m2p8l3fps3dal7h8gf9jvrv98tu3rqfdht86")

    assert AccAddress.validate("terra1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0tmam9")


def test_convert_from_val_address():
    assert (
        AccAddress.from_val_address(
            "terravaloper1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0yhqtk"
        )
        == "terra1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0tmam9"
    )


def test_validates_validator_address():
    assert not ValAddress.validate("terra1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0tmam9")
    assert not ValAddress.validate(
        "terravaloper1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0ygqtk"
    )  # bad checksum
    assert ValAddress.validate("terravaloper1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0yhqtk")


def test_convert_from_acc_address():
    assert (
        ValAddress.from_acc_address("terra1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0tmam9")
        == "terravaloper1pdx498r0hrc2fj36sjhs8vuhrz9hd2cw0yhqtk"
    )


def test_validates_acc_pubkey():
    assert not AccPubKey.validate(
        "terravaloperpub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5y7accr"
    )
    assert AccPubKey.validate(
        "terrapub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5nwzrf9"
    )


def test_converts_from_val_pubkey():
    assert (
        AccPubKey.from_val_pubkey(
            "terravaloperpub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5y7accr"
        )
        == "terrapub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5nwzrf9"
    )


def test_validates_val_pubkey():
    assert not ValPubKey.validate(
        "terrapub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5nwzrf9"
    )
    assert ValPubKey.validate(
        "terravaloperpub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5y7accr"
    )


def test_converts_from_acc_pubkey():
    assert (
        ValPubKey.from_acc_pubkey(
            "terrapub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5nwzrf9"
        )
        == "terravaloperpub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5y7accr"
    )
