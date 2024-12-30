from asyncua import Node
import logging
from production_line.equipment import Equipment


class Homogenizer(Equipment):
    def __init__(
        self,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
        variables: list[dict],
        properties: list[dict],
        methods: list[dict],
    ):
        super().__init__(
            "Homogenizer", logger, parent_node, idx, variables, properties, methods
        )

    async def initialize(self):
        await super().initialize()
