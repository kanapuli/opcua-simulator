from asyncua import Node
import logging
from .storage import Storage


class ColdStorage(Storage):
    """Cold Storage implementation"""

    def __init__(
        self,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
    ):
        variables = [
            {"temperature": 2.0},  # Initial temperature in °C
            {"capacity_utilization": 0.0},  # Initial capacity utilization in %
        ]

        properties = [
            {"min_temperature": -2.0},  # Minimum temperature
            {"max_temperature": 4.0},  # Maximum temperature
            {"total_capacity": 1000.0},  # Total storage capacity
        ]

        super().__init__(
            "Cold Storage", logger, parent_node, idx, variables, properties
        )

    async def initialize(self):
        await super().initialize()
        # Add any specific initialization for cold storage
