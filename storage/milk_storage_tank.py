from asyncua import Node
import logging
from .storage import Storage


class MilkStorageTank(Storage):
    """Milk Storage Tank implementation"""

    def __init__(
        self,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
    ):
        variables = [
            {"milk_volume": 0.0},  # Initial volume in liters
            {"temperature": 4.0},  # Initial temperature in °C
            {"status": False},  # False = Empty, True = Full
        ]

        properties = [
            {"max_capacity": 1000.0},  # Maximum capacity in liters
            {"min_temperature": 2.0},  # Minimum allowed temperature
            {"max_temperature": 6.0},  # Maximum allowed temperature
        ]

        super().__init__(
            "Milk Storage Tank", logger, parent_node, idx, variables, properties
        )

    async def initialize(self):
        await super().initialize()
        # Add any specific initialization for milk storage tank
