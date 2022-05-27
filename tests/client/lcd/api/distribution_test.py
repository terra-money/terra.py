from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bech32 import is_acc_address

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

def test_rewards():
    result = terra.distribution.rewards("terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e")
    assert result.total.to_data()


def test_validator_commission():
    result = terra.distribution.validator_commission(
        "terravaloper1thuj2a8sgtxr7z3gr39egng3syqqwas4hmvvlg"
    )
    assert result.to_data()


def test_withdraw_address():
    result = terra.distribution.withdraw_address(
        "terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e"
    )
    assert is_acc_address(result)


def test_comminity_pool():
    result = terra.distribution.community_pool()
    assert result.to_data()


def test_parameters():
    result = terra.distribution.parameters()
    assert result.get("community_tax")
    assert result.get("base_proposer_reward")
    assert result.get("bonus_proposer_reward")
    assert result.get("withdraw_addr_enabled")
