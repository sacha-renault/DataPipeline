from collections.abc import Callable
from .pipe_node import PipeNode

class InputNode(PipeNode):
    def __init__(self, name: str = "") -> None:
        super().__init__(None, None, f"Input {name}")