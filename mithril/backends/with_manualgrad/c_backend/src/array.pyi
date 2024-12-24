# Copyright 2022 Synnada, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import builtins
import ctypes
from collections.abc import Sequence
from types import EllipsisType
from typing import Any, overload

NestedList = list[float | "NestedList"]

lib: ctypes.CDLL

def to_c_int_array(lst) -> ctypes.c_int: ...
def to_c_float_array(arr) -> ctypes.c_float: ...

class Array(ctypes.Structure): ...

class PyArray:
    arr: Array
    shape: tuple[int, ...]
    ndim: int

    def data(self) -> NestedList: ...
    def __init__(self, arr: Array, shape: tuple[int, ...] | list[int]) -> None: ...
    def __gt__(self, other: PyArray) -> PyArray: ...
    def __ge__(self, other: PyArray) -> PyArray: ...
    def __lt__(self, other: PyArray) -> PyArray: ...
    def __le__(self, other: PyArray) -> PyArray: ...
    def __and__(self, other: PyArray) -> PyArray: ...
    def __or__(self, other: PyArray) -> PyArray: ...
    def __xor__(self, other: PyArray) -> PyArray: ...
    def __invert__(self) -> PyArray: ...
    def __matmul__(self, other: PyArray) -> PyArray: ...
    def __lshift__(self, other: PyArray) -> PyArray: ...
    def __rshift__(self, other: PyArray) -> PyArray: ...

    # Construction/Conversion methods
    def detach(self) -> PyArray: ...
    def numpy(self) -> Any: ...  # Returns numpy.ndarray
    def tolist(self) -> list[Any]: ...

    # Basic arithmetic operations
    def __add__(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def __sub__(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def __mul__(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def __pow__(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def __div__(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def __truediv__(
        self, other: PyArray | builtins.float | builtins.int
    ) -> PyArray: ...
    def __floordiv__(
        self, other: PyArray | builtins.float | builtins.int
    ) -> PyArray: ...
    def __neg__(self) -> PyArray: ...

    # Inplace operations
    def add_(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def sub_(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def mul_(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def div_(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...

    # Shape operations
    def reshape(
        self, *shape: builtins.int | list[builtins.int] | tuple[builtins.int, ...]
    ) -> PyArray: ...
    def squeeze(self, dim: builtins.int | None = None) -> PyArray: ...
    def unsqueeze(self, dim: builtins.int) -> PyArray: ...
    @overload
    def transpose(self, axes: None | Sequence[int]) -> PyArray: ...
    @overload
    def transpose(self, *axes: int) -> PyArray: ...
    def permute(self, *dims: builtins.int) -> PyArray: ...
    def flatten(
        self, start_dim: builtins.int = 0, end_dim: builtins.int = -1
    ) -> PyArray: ...

    # Item extraction methods
    def item(self) -> int | float | bool: ...

    # Indexing
    def __getitem__(
        self,
        idx: slice
        | int
        | EllipsisType
        | tuple[slice | int | None | EllipsisType | PyArray, ...]
        | PyArray
        | None,
    ) -> PyArray: ...
    def __setitem__(
        self,
        idx: builtins.int | slice | PyArray | tuple[Any, ...],
        val: PyArray | builtins.float | builtins.int,
    ) -> None: ...
    def index_select(self, dim: builtins.int, index: PyArray) -> PyArray: ...
    def masked_select(self, mask: PyArray) -> PyArray: ...

    # Reduction operations
    def max(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray | tuple[PyArray, PyArray]: ...
    def min(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray | tuple[PyArray, PyArray]: ...
    def argmax(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray: ...
    def argmin(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray: ...

    # Linear algebra operations
    def matmul(self, other: PyArray) -> PyArray: ...
    def mm(self, other: PyArray) -> PyArray: ...
    def bmm(self, other: PyArray) -> PyArray: ...
    def dot(self, other: PyArray) -> PyArray: ...

    # Statistical operations
    def normal_(self, mean: builtins.float = 0, std: builtins.float = 1) -> PyArray: ...
    def uniform_(
        self, from_: builtins.float = 0, to: builtins.float = 1
    ) -> PyArray: ...
    def bernoulli_(self, p: builtins.float = 0.5) -> PyArray: ...

    # Gradient operations
    def backward(self, gradient: PyArray | None = None) -> None: ...
    def grad(self) -> PyArray | None: ...
    def requires_grad_(self, requires_grad: bool = True) -> PyArray: ...
    def detach_(self) -> PyArray: ...
    def retain_grad(self) -> None: ...

    # Properties

    @property
    def T(self) -> PyArray: ...  # noqa: N802
    @property
    def H(self) -> PyArray: ...  # noqa: N802 Conjugate transpose
    # @property
    # def shape(self) -> tuple: ...
    @property
    def dtype(self) -> Any: ...
    @property
    def device(self) -> Any: ...
    @property
    def requires_grad(self) -> bool: ...
    @property
    def is_leaf(self) -> bool: ...
    # @property
    # def data(self) -> PyArray: ...
    # Type conversion
    def bool(self) -> PyArray: ...
    def int(self) -> PyArray: ...
    def long(self) -> PyArray: ...
    def float(self) -> PyArray: ...
    def double(self) -> PyArray: ...
    def half(self) -> PyArray: ...

    # Other operations
    def abs(self) -> PyArray: ...
    def sqrt(self) -> PyArray: ...
    def exp(self) -> PyArray: ...
    def log(self) -> PyArray: ...
    def sin(self) -> PyArray: ...
    def cos(self) -> PyArray: ...
    def tan(self) -> PyArray: ...
    def ceil(self) -> PyArray: ...
    def floor(self) -> PyArray: ...
    def round(self) -> PyArray: ...
    def clip(
        self, min: builtins.float | None = None, max: builtins.float | None = None
    ) -> PyArray: ...
    def zero_(self) -> PyArray: ...
    def fill_(self, value: builtins.float) -> PyArray: ...

    # Comparison operations
    def eq(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def ne(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def lt(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def le(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def gt(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def ge(self, other: PyArray | builtins.float | builtins.int) -> PyArray: ...
    def all(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray: ...
    def any(
        self, dim: builtins.int | None = None, keepdim: builtins.bool = False
    ) -> PyArray: ...

    # Size/shape inspection
    def dim(self) -> builtins.int: ...
    def size(
        self, dim: builtins.int | None = None
    ) -> builtins.int: ...  # TODO: Check if return is correct
    def swapaxes(self, idx1: builtins.int, idx2: builtins.int) -> PyArray: ...

    # Special dunder methods
    def __len__(self) -> builtins.int: ...
    def __bool__(self) -> builtins.bool: ...
    def __iter__(self) -> Any: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

def empty(shape: tuple[builtins.int, ...] | list[builtins.int]) -> PyArray: ...
def ones(shape: tuple[builtins.int, ...] | list[builtins.int]) -> PyArray: ...
def zeros(shape: tuple[builtins.int, ...] | list[builtins.int]) -> PyArray: ...
