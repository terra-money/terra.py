"""Block transformers.

A function that is called after the block has been fetched and deserialized,
to transform the block data and add more info, such as turning Amino-encoded
TXs from TxInfo's __rawtx__ (if it exists) into full TxInfo data.

The default behavior is to fetch all the transactions by their hash, because
we do not yet have the means to decode Amino from Python. Having one would
immensely boost performance for block-related queries. Feel free to disable
this automatic behavior by setting your Terra instance to not fetch transactions.

(see `fetch_txs_transformer`)

You can also swap out the `transform_block` function with your own implementation,
    which should implement the signature:

    def my_transformer(terra: terra_sdk.Terra, block: terra_sdk.core.Block) -> terra_sdk.core.Block

Swapping out this functionality:

>>> terra.blocks.transformer = my_transformer

And voila! You should get your transform block as the result of any queries!
"""

from terra_sdk.core import Block
# TODO: add more efficient block transformer by adding go-amino bindings for Python
from terra_sdk.query.txinfo import TxInfosQuery
from terra_sdk.util import hash_amino

__all__ = ["FetchTxInfoBlockTransformer"]


class FetchTxInfoBlockTransformer:
    """Fetches TxInfo from data in `block.txs`, which it expects to contain Amino-encoded
    TX data."""

    def __init__(self, terra):
        self.terra = terra  # need terra instance to fetch txinfo

    def __call__(self, block: Block) -> Block:
        txhashes = [hash_amino(txdata) for txdata in block.txs]
        txs = self.terra.tx._tx_info_threaded(txhashes)
        block.txs = TxInfosQuery(txs)
        return block
