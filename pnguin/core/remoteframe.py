import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError

from pnguin.models import Axis
from pnguin.api import connect


class RemoteFrame:
    @validate_arguments
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.connection = connect(conn_string)
