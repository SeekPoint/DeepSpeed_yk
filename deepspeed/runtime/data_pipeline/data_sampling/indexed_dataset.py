# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team
"""
Part of this code was adopted from https://github.com/NVIDIA/Megatron-LM/blob/main/megatron/data/indexed_dataset.py
"""

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# copied from fairseq/fairseq/data/indexed_dataset.py
# Removed IndexedRawTextDataset since it relied on Fairseq dictionary
# other slight modifications to remove fairseq dependencies
# Added document index to index file and made it accessible.
#    An empty sentence no longer separates documents.

# Some of the fixes/improvements are adopted from
# https://github.com/bigscience-workshop/Megatron-DeepSpeed/blob/main/megatron/data/indexed_dataset.py

from functools import lru_cache
import os
import shutil
import struct
from itertools import accumulate

import numpy as np
import torch
from pydebug import gd, infoTensor

def __best_fitting_dtype(vocab_size=None):
    if vocab_size is not None and vocab_size < 65500:
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return np.uint16
    else:
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return np.int32


def get_available_dataset_impl():
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    return ['lazy', 'cached', 'mmap']


def infer_dataset_impl(path):
    if IndexedDataset.exists(path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        with open(index_file_path(path), 'rb') as f:
            magic = f.read(8)
            if magic == IndexedDataset._HDR_MAGIC:
                return 'cached'
            elif magic == MMapIndexedDataset.Index._HDR_MAGIC[:8]:
                return 'mmap'
            else:
                return None
    else:
        print(f"Dataset does not exist: {path}")
        print("Path should be a basename that both .idx and .bin can be appended to get full filenames.")
        return None


def make_builder(out_file, impl, vocab_size=None):
    if impl == 'mmap':
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return MMapIndexedDatasetBuilder(out_file, dtype=__best_fitting_dtype(vocab_size))
    else:
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return IndexedDatasetBuilder(out_file)


def make_dataset(path, impl, skip_warmup=False):
    if not IndexedDataset.exists(path):
        print(f"Dataset does not exist: {path}")
        print("Path should be a basename that both .idx and .bin can be appended to get full filenames.")
        return None
    if impl == 'infer':
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        impl = infer_dataset_impl(path)
    if impl == 'lazy' and IndexedDataset.exists(path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return IndexedDataset(path)
    elif impl == 'cached' and IndexedDataset.exists(path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return IndexedCachedDataset(path)
    elif impl == 'mmap' and MMapIndexedDataset.exists(path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return MMapIndexedDataset(path, skip_warmup)
    print(f"Unknown dataset implementation: {impl}")
    return None


def dataset_exists(path, impl):
    if impl == 'mmap':
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return MMapIndexedDataset.exists(path)
    else:
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        return IndexedDataset.exists(path)


def read_longs(f, n):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    a = np.empty(n, dtype=np.int64)
    f.readinto(a)
    return a


def write_longs(f, a):
    f.write(np.array(a, dtype=np.int64))


dtypes = {
    1: np.uint8,
    2: np.int8,
    3: np.int16,
    4: np.int32,
    5: np.int64,
    6: np.float64,
    7: np.double,
    8: np.uint16,
    9: np.uint32,
    10: np.uint64
}


def code(dtype):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    for k in dtypes.keys():
        if dtypes[k] == dtype:
            return k
    raise ValueError(dtype)


def index_file_path(prefix_path):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    return prefix_path + '.idx'


def data_file_path(prefix_path):
    return prefix_path + '.bin'


def create_doc_idx(sizes):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    doc_idx = [0]
    for i, s in enumerate(sizes):
        if s == 0:
            doc_idx.append(i + 1)
    return doc_idx


class IndexedDataset(torch.utils.data.Dataset):
    """Loader for IndexedDataset"""
    _HDR_MAGIC = b'TNTIDX\x00\x00'

    def __init__(self, path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        super().__init__()
        self.path = path
        self.data_file = None
        self.read_index(path)

    def read_index(self, path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        with open(index_file_path(path), 'rb') as f:
            magic = f.read(8)
            assert magic == self._HDR_MAGIC, ('Index file doesn\'t match expected format. '
                                              'Make sure that --dataset-impl is configured properly.')
            version = f.read(8)
            assert struct.unpack('<Q', version) == (1, )
            code, self.element_size = struct.unpack('<QQ', f.read(16))
            self.dtype = dtypes[code]
            self._len, self.s = struct.unpack('<QQ', f.read(16))
            self.doc_count = struct.unpack('<Q', f.read(8))
            self.dim_offsets = read_longs(f, self._len + 1)
            self.data_offsets = read_longs(f, self._len + 1)
            self.sizes = read_longs(f, self.s)
            self.doc_idx = read_longs(f, self.doc_count)

    def read_data(self, path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self.data_file = open(data_file_path(path), 'rb', buffering=0)

    def check_index(self, i):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        if i < 0 or i >= self._len:
            raise IndexError('index out of range')

    def __del__(self):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        if self.data_file:
            self.data_file.close()

    # @lru_cache(maxsize=8)
    def __getitem__(self, idx):
        if not self.data_file:
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            self.read_data(self.path)
        if isinstance(idx, int):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            i = idx
            self.check_index(i)
            tensor_size = self.sizes[self.dim_offsets[i]:self.dim_offsets[i + 1]]
            a = np.empty(tensor_size, dtype=self.dtype)
            self.data_file.seek(self.data_offsets[i] * self.element_size)
            self.data_file.readinto(a)
            return a
        elif isinstance(idx, slice):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            start, stop, step = idx.indices(len(self))
            if step != 1:
                raise ValueError("Slices into indexed_dataset must be contiguous")
            sizes = self.sizes[self.dim_offsets[start]:self.dim_offsets[stop]]
            size = sum(sizes)
            a = np.empty(size, dtype=self.dtype)
            self.data_file.seek(self.data_offsets[start] * self.element_size)
            self.data_file.readinto(a)
            offsets = list(accumulate(sizes))
            sents = np.split(a, offsets[:-1])
            return sents

    def __len__(self):
        return self._len

    def num_tokens(self, index):
        return self.sizes[index]

    def size(self, index):
        return self.sizes[index]

    @staticmethod
    def exists(path):
        return (os.path.exists(index_file_path(path)) and os.path.exists(data_file_path(path)))

    @property
    def supports_prefetch(self):
        return False  # avoid prefetching to save memory


class IndexedCachedDataset(IndexedDataset):

    def __init__(self, path):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        super().__init__(path)
        self.cache = None
        self.cache_index = {}

    @property
    def supports_prefetch(self):
        return True

    def prefetch(self, indices):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        if all(i in self.cache_index for i in indices):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            return
        if not self.data_file:
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            self.read_data(self.path)
        indices = sorted(set(indices))
        total_size = 0
        for i in indices:
            total_size += self.data_offsets[i + 1] - self.data_offsets[i]
        self.cache = np.empty(total_size, dtype=self.dtype)
        ptx = 0
        self.cache_index.clear()
        for i in indices:
            self.cache_index[i] = ptx
            size = self.data_offsets[i + 1] - self.data_offsets[i]
            a = self.cache[ptx:ptx + size]
            self.data_file.seek(self.data_offsets[i] * self.element_size)
            self.data_file.readinto(a)
            ptx += size
        if self.data_file:
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            # close and delete data file after prefetch so we can pickle
            self.data_file.close()
            self.data_file = None

    # @lru_cache(maxsize=8)
    def __getitem__(self, idx):
        if isinstance(idx, int):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            i = idx
            self.check_index(i)
            tensor_size = self.sizes[self.dim_offsets[i]:self.dim_offsets[i + 1]]
            a = np.empty(tensor_size, dtype=self.dtype)
            ptx = self.cache_index[i]
            np.copyto(a, self.cache[ptx:ptx + a.size])
            return a
        elif isinstance(idx, slice):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            # Hack just to make this work, can optimizer later if necessary
            sents = []
            for i in range(*idx.indices(len(self))):
                sents.append(self[i])
            return sents


class IndexedDatasetBuilder(object):
    element_sizes = {np.uint8: 1, np.int8: 1, np.int16: 2, np.int32: 4, np.int64: 8, np.float64: 4, np.double: 8}

    def __init__(self, out_file, dtype=np.int32):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self.out_file = open(out_file, 'wb')
        self.dtype = dtype
        self.data_offsets = [0]
        self.dim_offsets = [0]
        self.sizes = []
        self.element_size = self.element_sizes[self.dtype]
        self.doc_idx = [0]

    def add_item(self, tensor):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        bytes = self.out_file.write(np.array(tensor.numpy(), dtype=self.dtype))
        self.data_offsets.append(self.data_offsets[-1] + bytes / self.element_size)
        for s in tensor.size():
            self.sizes.append(s)
        self.dim_offsets.append(self.dim_offsets[-1] + len(tensor.size()))

    def end_document(self):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self.doc_idx.append(len(self.sizes))

    def merge_file_(self, another_file):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        index = IndexedDataset(another_file)
        assert index.dtype == self.dtype

        doc_offset = len(self.sizes)

        begin = self.data_offsets[-1]
        for data_offset in index.data_offsets[1:]:
            self.data_offsets.append(begin + data_offset)
        self.sizes.extend(index.sizes)
        begin = self.dim_offsets[-1]
        for dim_offset in index.dim_offsets[1:]:
            self.dim_offsets.append(begin + dim_offset)
        self.doc_idx.extend((doc_offset + index.doc_idx)[1:])

        with open(data_file_path(another_file), 'rb') as f:
            while True:
                data = f.read(1024)
                if data:
                    self.out_file.write(data)
                else:
                    break

    def finalize(self, index_file):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self.out_file.close()
        index = open(index_file, 'wb')
        index.write(b'TNTIDX\x00\x00')
        index.write(struct.pack('<Q', 1))
        index.write(struct.pack('<QQ', code(self.dtype), self.element_size))
        index.write(struct.pack('<QQ', len(self.data_offsets) - 1, len(self.sizes)))
        index.write(struct.pack('<Q', len(self.doc_idx)))
        write_longs(index, self.dim_offsets)
        write_longs(index, self.data_offsets)
        write_longs(index, self.sizes)
        write_longs(index, self.doc_idx)
        index.close()


def _warmup_mmap_file(path):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    with open(path, 'rb') as stream:
        while stream.read(100 * 1024 * 1024):
            pass


def exscan_from_cumsum_(arr):
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
    # given an array holding the result of an inclusive scan (cumsum),
    # convert to an exclusive scan (shift to the right)
    # [10, 30, 35, 50] --> [0, 10, 30, 35]
    if arr.size > 1:
        arr[1:] = arr[:-1]
    if arr.size > 0:
        arr[0] = 0


def get_pointers_with_total(sizes, elemsize, dtype):
    """Return a numpy array of type np.dtype giving the byte offsets.

    Multiplies values in the sizes array by elemsize (bytes),
    and then computes an exclusive scan to get byte offsets.
    Returns the total number of bytes as second item in a tuple.
    """
    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')

    # scale values in sizes array by elemsize to get sizes in bytes
    pointers = np.array(sizes, dtype=dtype)
    pointers *= elemsize
    np.cumsum(pointers, axis=0, out=pointers)

    # get total number of bytes from all sizes (last element)
    bytes_last = pointers[-1] if len(sizes) > 0 else 0

    # convert to byte offsets
    exscan_from_cumsum_(pointers)

    return pointers, bytes_last


class MMapIndexedDataset(torch.utils.data.Dataset):

    class Index(object):
        _HDR_MAGIC = b'MMIDIDX\x00\x00'

        @classmethod
        def writer(cls, path, dtype):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')

            class _Writer(object):

                def __enter__(self):
                    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
                    self._file = open(path, 'wb')

                    self._file.write(cls._HDR_MAGIC)
                    self._file.write(struct.pack('<Q', 1))
                    self._file.write(struct.pack('<B', code(dtype)))

                    return self

                @staticmethod
                def _get_pointers(sizes, npdtype):
                    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
                    """Return a numpy array of byte offsets given a list of sizes.

                    Multiplies values in the sizes array by dtype size (bytes),
                    and then computes an exclusive scan to get byte offsets.
                    """

                    # compute element sizes in bytes
                    pointers, _ = get_pointers_with_total(sizes, dtype().itemsize, npdtype)
                    return pointers

                def write(self, sizes, doc_idx):
                    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
                    self._file.write(struct.pack('<Q', len(sizes)))
                    self._file.write(struct.pack('<Q', len(doc_idx)))

                    sizes32 = np.array(sizes, dtype=np.int32)
                    self._file.write(sizes32.tobytes(order='C'))
                    del sizes32

                    pointers = self._get_pointers(sizes, np.int64)
                    del sizes
                    self._file.write(pointers.tobytes(order='C'))
                    del pointers

                    doc_idx = np.array(doc_idx, dtype=np.int64)
                    self._file.write(doc_idx.tobytes(order='C'))

                def __exit__(self, exc_type, exc_val, exc_tb):
                    gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
                    self._file.close()

            return _Writer()

        def __init__(self, path, skip_warmup=False):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            with open(path, 'rb') as stream:
                magic_test = stream.read(9)
                assert self._HDR_MAGIC == magic_test, ('Index file doesn\'t match expected format. '
                                                       'Make sure that --dataset-impl is configured properly.')
                version = struct.unpack('<Q', stream.read(8))
                assert (1, ) == version

                dtype_code, = struct.unpack('<B', stream.read(1))
                self._dtype = dtypes[dtype_code]
                self._dtype_size = self._dtype().itemsize

                self._len = struct.unpack('<Q', stream.read(8))[0]
                self._doc_count = struct.unpack('<Q', stream.read(8))[0]
                offset = stream.tell()

            if not skip_warmup:
                print("    warming up index mmap file...")
                _warmup_mmap_file(path)

            self._bin_buffer_mmap = np.memmap(path, mode='r', order='C')
            self._bin_buffer = memoryview(self._bin_buffer_mmap)
            print("    reading sizes...")
            self._sizes = np.frombuffer(self._bin_buffer, dtype=np.int32, count=self._len, offset=offset)
            print("    reading pointers...")
            self._pointers = np.frombuffer(self._bin_buffer,
                                           dtype=np.int64,
                                           count=self._len,
                                           offset=offset + self._sizes.nbytes)
            print("    reading document index...")
            self._doc_idx = np.frombuffer(self._bin_buffer,
                                          dtype=np.int64,
                                          count=self._doc_count,
                                          offset=offset + self._sizes.nbytes + self._pointers.nbytes)

        def __del__(self):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            self._bin_buffer_mmap._mmap.close()
            del self._bin_buffer_mmap

        @property
        def dtype(self):
            return self._dtype

        @property
        def sizes(self):
            return self._sizes

        @property
        def doc_idx(self):
            return self._doc_idx

        @lru_cache(maxsize=8)
        def __getitem__(self, i):
            return self._pointers[i], self._sizes[i]

        def __len__(self):
            return self._len

    def __init__(self, path, skip_warmup=False):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        super().__init__()

        self._path = None
        self._index = None
        self._bin_buffer = None

        self._do_init(path, skip_warmup)

    def __getstate__(self):
        return self._path

    def __setstate__(self, state):
        self._do_init(state)

    def _do_init(self, path, skip_warmup):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self._path = path
        self._index = self.Index(index_file_path(self._path), skip_warmup)

        if not skip_warmup:
            print("    warming up data mmap file...")
            _warmup_mmap_file(data_file_path(self._path))
        print("    creating numpy buffer of mmap...")
        self._bin_buffer_mmap = np.memmap(data_file_path(self._path), mode='r', order='C')
        print("    creating memory view of numpy buffer...")
        self._bin_buffer = memoryview(self._bin_buffer_mmap)

    def __del__(self):
        self._bin_buffer_mmap._mmap.close()
        del self._bin_buffer_mmap
        del self._index

    def __len__(self):
        return len(self._index)

    # @lru_cache(maxsize=8)
    def __getitem__(self, idx):
        if isinstance(idx, int):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            ptr, size = self._index[idx]
            np_array = np.frombuffer(self._bin_buffer, dtype=self._index.dtype, count=size, offset=ptr)
            return np_array
        elif isinstance(idx, slice):
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            start, stop, step = idx.indices(len(self))
            if step != 1:
                raise ValueError("Slices into indexed_dataset must be contiguous")
            ptr = self._index._pointers[start]
            sizes = self._index._sizes[idx]
            offsets = list(accumulate(sizes))
            total_size = sum(sizes)
            np_array = np.frombuffer(self._bin_buffer, dtype=self._index.dtype, count=total_size, offset=ptr)
            sents = np.split(np_array, offsets[:-1])
            return sents

    def get(self, idx, offset=0, length=None):
        """ Retrieves a single item from the dataset with the option to only
        return a portion of the item.

        get(idx) is the same as [idx] but get() does not support slicing.
        """
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        ptr, size = self._index[idx]
        if length is None:
            length = size - offset
        ptr += offset * np.dtype(self._index.dtype).itemsize
        np_array = np.frombuffer(self._bin_buffer, dtype=self._index.dtype, count=length, offset=ptr)
        return np_array

    @property
    def sizes(self):
        return self._index.sizes

    def size(self, index):
        return self._index.sizes[index]

    @property
    def doc_idx(self):
        return self._index.doc_idx

    def get_doc_idx(self):
        return self._index._doc_idx

    def set_doc_idx(self, doc_idx_):
        self._index._doc_idx = doc_idx_

    @property
    def supports_prefetch(self):
        return False

    @staticmethod
    def exists(path):
        return (os.path.exists(index_file_path(path)) and os.path.exists(data_file_path(path)))

    @property
    def dtype(self):
        return self._index.dtype


class MMapIndexedDatasetBuilder(object):

    def __init__(self, out_file, dtype=np.int64):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self._data_file = open(out_file, 'wb')
        self._dtype = dtype
        self._sizes = []
        self._doc_idx = [0]

    def add_item(self, tensor):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        np_array = np.array(tensor.numpy(), dtype=self._dtype)
        self._data_file.write(np_array.tobytes(order='C'))
        self._sizes.append(np_array.size)

    def add_item_numpy(self, np_array):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        if np_array.dtype != self._dtype:
            gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
            np_array = np_array.astype(self._dtype)
        self._data_file.write(np_array.tobytes(order='C'))
        self._sizes.append(np_array.size)

    def end_document(self):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self._doc_idx.append(len(self._sizes))

    def merge_file_(self, another_file):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        # Concatenate index
        index = MMapIndexedDataset.Index(index_file_path(another_file))
        assert index.dtype == self._dtype

        total_len = len(index.sizes) + len(self._sizes)
        print(f"    concat {another_file} size={len(index.sizes)} for a total size of {total_len}")

        offset = len(self._sizes)
        self._sizes.extend(index.sizes)
        self._doc_idx.extend((offset + index.doc_idx)[1:])

        # Concatenate data
        with open(data_file_path(another_file), 'rb') as f:
            shutil.copyfileobj(f, self._data_file)

    def finalize(self, index_file):
        gd.debuginfo(prj='ds', info=self.__class__.__name__ if 'self' in locals() or 'self' in globals() else '')
        self._data_file.close()

        with MMapIndexedDataset.Index.writer(index_file, self._dtype) as index:
            index.write(self._sizes, self._doc_idx)
