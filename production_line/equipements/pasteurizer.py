from typing import Callable
from asyncua import Node
import logging
from production_line.equipment import Equipment


class Pasteurizer(Equipment):
    def __init__(
        self,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
        variables: list[dict[str, any]],
        properties: list[dict[str, any]],
        methods: list[dict[str, Callable[[], any]]],
    ):
        super().__init__(
            "Pasteurizer", logger, parent_node, idx, variables, properties, methods
        )

    async def initialize(self):
        await super().initialize()
