from __future__ import annotations

from pnguin.models import Axis
from pnguin.core.filter import Filter

from typing import Callable


class Frame:
    def head(self, n: int = 5):
        pass

    def dropna(self, exclude: list = [], inplace: bool = False):
        pass

    def apply(self, x: Callable, axis: Axis = Axis.col, inplace: bool = False):
        pass

    def filter(self, filter: Filter):
        pass

    def iterate(self):
        pass

    def to_csv(self, filename: str):
        pass

    def to_db(self):
        pass


class RemoteFrame:
    def head(self, n: int = 5) -> Frame:
        pass

    def dropna(self, exclude: list = []) -> Frame:
        pass

    def apply(self, x: Callable, axis: Axis = Axis.col) -> Frame:
        pass

    def to_csv(self, filename: str) -> Frame:
        pass

    def to_df(self, axis: Axis) -> Frame:
        pass

    def __getitem__(self, key) -> RemoteFrame:
        pass

    def __setitem__(self, key, value) -> Frame:
        pass
