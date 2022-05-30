"""Useful contract-related functions."""

import base64
from typing import Dict, List, Union

from terra_sdk.core import AccAddress
from terra_sdk.core.auth import TxInfo
from terra_sdk.core.broadcast import BlockTxBroadcastResult

__all__ = [
    "read_file_as_b64",
    "get_code_id",
    "get_contract_address",
    "get_contract_events",
]


def read_file_as_b64(path: Union[str, bytes, int]) -> str:
    """Reads a file's contents as binary bytes and encodes it in a base64-string.

    Args:
        path (Union[str, bytes, int]): binary file path

    Returns:
        str: file's bytes in base64-encoded string
    """
    with open(path, "rb") as contract_file:
        contract_bytes = base64.b64encode(contract_file.read()).decode()
        return contract_bytes


def get_code_id(
    tx_result: Union[BlockTxBroadcastResult, TxInfo], msg_index: int = 0
) -> str:
    """Utility function for extracting the code id from a ``MsgStoreCode`` message.

    Args:
        tx_result (BlockTxBroadcastResult): broadcast result
        msg_index (int, optional): index of ``MsgStoreCode`` inside tx. Defaults to 0.

    Returns:
        str: extracted code id
    """
    if tx_result.logs:
        code_id = tx_result.logs[msg_index].events_by_type["store_code"]["code_id"][0]
        return code_id
    else:
        raise ValueError("could not parse code id -- tx logs are empty.")


def get_contract_address(
    tx_result: Union[BlockTxBroadcastResult, TxInfo], msg_index: int = 0
) -> AccAddress:
    """Utility function for extracting the contract address from a ``MsgInstantiateContract``
    message.

    Args:
        tx_result (BlockTxBroadcastResult): broadcast result
        msg_index (int, optional): index of ``MsgInstantiateContract`` inside tx. Defaults to 0.

    Returns:
        str: extracted contract address
    """
    if tx_result.logs:
        contract_address = tx_result.logs[msg_index].events_by_type["wasm"][
            "_contract_address"
        ][0]
        return AccAddress(contract_address)
    else:
        raise ValueError("could not parse code id -- tx logs are empty.")


def get_contract_events(
    tx_result: Union[BlockTxBroadcastResult, TxInfo], msg_index: int = 0
) -> List[Dict[str, str]]:
    if tx_result.logs:
        contract_events = []
        for event in tx_result.logs[msg_index].events:
            if event["type"] == "from_contract":
                event_data: Dict[str, str] = {}
                current_contract_address = event["attributes"][0]["value"]
                for att in event["attributes"]:
                    if (
                        att["key"] == "contract_address"
                        and current_contract_address != att["value"]
                    ):
                        contract_events.append(event_data)
                        event_data = {}
                        current_contract_address = att["value"]
                    event_data[att["key"]] = att["value"]
                contract_events.append(event_data)  # append remaining
                return contract_events
        raise ValueError("could not find event type 'from_contract' in logs")
    else:
        raise ValueError("could not parse contract events -- tx logs are empty.")
