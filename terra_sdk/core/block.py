from typing import List

import attr

__all__ = [
    "BlockInfo",
    "Block",
    "Header",
    "Evidence",
    "BlockID",
    "Parts",
    "Version",
    "LastCommit",
    "Signature",
]


@attr.s
class Evidence:
    evidence: List[str] = attr.ib(converter=list)


@attr.s
class Version:
    block: str = attr.ib()
    app: str = attr.ib()


@attr.s
class Parts:
    total: str = attr.ib()
    hash: str = attr.ib()


@attr.s
class BlockID:
    hash: str = attr.ib()
    part_set_header: Parts = attr.ib()


@attr.s
class Header:
    version: Version = attr.ib()
    chain_id: str = attr.ib()
    height: str = attr.ib()
    time: str = attr.ib()
    last_block_id: BlockID = attr.ib()
    last_commit_hash: str = attr.ib()
    data_hash: str = attr.ib()
    validators_hash: str = attr.ib()
    next_validators_hash: str = attr.ib()
    consensus_hash: str = attr.ib()
    app_hash: str = attr.ib()
    last_results_hash: str = attr.ib()
    evidence_hash: str = attr.ib()
    proposer_address: str = attr.ib()


@attr.s
class Signature:
    block_id_flag: int = attr.ib(converter=int)
    validator_address: str = attr.ib()
    timestamp: str = attr.ib()
    signature: str = attr.ib()


@attr.s
class LastCommit:
    height: str = attr.ib()
    round: int = attr.ib(converter=int)
    block_id: BlockID = attr.ib()
    signatures: List[Signature] = attr.ib()


@attr.s
class Block:
    header: Header = attr.ib()
    data: List[str] = attr.ib()
    evidence: Evidence = attr.ib()
    last_commit: LastCommit = attr.ib()


@attr.s
class BlockInfo:
    block_id: BlockID = attr.ib()
    block: Block = attr.ib()
