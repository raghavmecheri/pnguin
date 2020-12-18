from pnguin.models import Axis
from typing import Callable


class Frame:
    def head(self, n: int = 5):
        pass

    def dropna(self, exclude: list = [], inplace: bool = False):
        pass

    def apply(self, x: Callable, axis: Axis = Axis.col, inplace: bool = False):
        pass

    def to_csv(self):
        pass

    def to_db(self):
        pass
