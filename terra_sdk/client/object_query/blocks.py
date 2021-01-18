"""Classes for handling logic of block fetching."""

from multiprocessing.pool import ThreadPool
from typing import Union

from terra_sdk.client.lcd.api import project
from terra_sdk.core import Block
from terra_sdk.transform.block import FetchTxInfoBlockTransformer

# TODO: rename to BlocksAPI ?

__all__ = ["BlocksQuery", "BlocksRange"]


class BlocksRange(object):
    def __init__(
        self, blocks, start_height: int = None, stop_height: int = None, step: int = 1
    ):
        """Creates a generator that iterates over [start_height, until_height]. Note that
        this goes against the convention that ranges should be [start, end); however humans
        think in inclusive intervals for block height.
        """
        self.blocks = blocks
        self.start_height = start_height or 1
        self.stop_height = stop_height or len(self.blocks)
        self.step = step
        self._range = range(self.start_height, self.stop_height + 1, self.step)

    def __repr__(self):
        s = self
        return f"BlocksRange(start_height={s.start_height!r}, stop_height={s.stop_height!r}, step={s.step!r})"

    def __iter__(self):
        yield from self.__next__()

    def __next__(self):
        for i in self._range:
            yield self.blocks.at(i)

    def threads(self, num_threads: int = 1):
        """Creates a multithreaded iterator to fetch blocks more quickly."""
        return ThreadPool(num_threads).imap(lambda i: self.blocks.at(i), self._range)


class BlocksQuery(object):
    """Manages how blocks are retrieved and parsed from the blockchain."""

    def __init__(self, terra):
        self.terra = terra
        self.transform_after_fetch = True
        self.transformer = FetchTxInfoBlockTransformer(terra)

    def _normalize_index(self, index: int):
        """Changes negative indices to positive ones."""
        if index < 0:
            return len(self) + index
        else:
            return index

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, int):
            return self.at(self._normalize_index(key) + 1)
        elif isinstance(key, slice):
            start = self._normalize_index(key.start) + 1 if key.start else None
            stop = self._normalize_index(key.stop) + 1 if key.stop else len(self)
            step = key.step if key.step else 1
            return self.range(start, stop, step)
        else:
            raise TypeError(
                "invalid type for blocks[key], `key` must be <int> or <slice>"
            )

    def at(self, height: int):
        """Get the raw block data from the Tendermint API and deserializes it into a
        Block object. Applies the transformer(block) function to the block
        before returning.
        """
        res = self.terra._tendermint.block(height)  # block data
        block = Block.deserialize(res)
        if self.transform_after_fetch:
            block = self.transformer(block)
        return project(res, block)

    def range(
        self,
        start_height: int = None,
        stop_height: int = None,
        step: int = 1,
        threads: int = 1,
    ):
        # this mimics the python behavior: range(4) = range(0, 4); range(4, 8) = range(4, 8)
        result = BlocksRange(self, start_height, stop_height, step)
        if start_height is None:
            result = BlocksRange(self, None, None, step)
        if stop_height is None:
            result = BlocksRange(self, 1, start_height, step)
        if threads < 2:
            return result
        else:
            return result.threads(threads)

    def __call__(
        self, start_height: int, stop_height: int, step: int = 1, threads: int = 1
    ):
        return self.range(start_height, stop_height, step, threads)

    def __len__(self):
        res = self.terra._tendermint.block()  # get latest block
        return project(res, int(res.block.header.height))

    def threads(self, num_threads: int = 1):
        return self.range().threads(num_threads)
