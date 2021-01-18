import pytest

from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.util.validation import is_acc_address, is_val_address


def compare(k: MnemonicKey, data: dict):
    assert k.mnemonic == data["mnemonic"]
    assert k.acc_address == data["address"]
    assert k.val_address == data["val_address"]
    assert k.acc_pubkey == data["pubkey"]
    assert k.val_pubkey == data["val_pubkey"]


class TestMnemonicKeyDerivation:
    """Tests ability to derive correct public / private key pair from a mnemonic."""

    # TODO: Key derivation for account, index other than (0, 0)

    def test_from_mnemonic(self, mnemonics):
        """Test whether creating a MnemonicKey with a known mnemonic generates the correct values."""
        # GIVEN a 24-character mnemonic
        # THEN give back a correctly-populated MnemonicKey
        for mnemonic in mnemonics:
            k = MnemonicKey(mnemonic["mnemonic"])
            compare(k, mnemonic)

    def test_generate(self):
        """Test whether random Mnemonic generation works."""
        k = MnemonicKey.generate()
        assert len(k.mnemonic.split()) == 24
        assert k.mnemonic != MnemonicKey.generate().mnemonic
        assert is_acc_address(k.acc_address)
        assert is_val_address(k.val_address)
