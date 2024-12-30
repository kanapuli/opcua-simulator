import logging
from production_line.equipment import Equipment
from asyncua import Node, ua
import asyncio
import random


class ProductionLine:
    """
    Represents a single production line (a whole production line)
    Example:
    - Milk processing line
    - Cheese processing line
    - Yogurt processing line

    Attributes:
    - _batch_id: str (unique identifier for the batch)
    - _production_rate: float (production rate in units per second)
    - _efficiency: float (efficiency percentage of the production line)
    """

    _batch_id: str = ""
    _production_rate: float = 0.0
    _efficiency: float = 0.0
    _instance = None

    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
    ):
        self.name = name
        self._logger = logger
        self._parent_node = parent_node
        self._idx = idx
        self.node: Node = None

    def start_batch(self, batch_id: str):
        self._batch_id = batch_id
        self._production_rate = 1.0
        self._efficiency = 1.0

    def stop_batch(self):
        self._batch_id = ""
        self._production_rate = 0.0
        self._efficiency = 0.0

    async def initialize(self):
        """Create a node object for the production line"""
        self.node = await self._parent_node.add_object(self._idx, self.name)
        self._logger.info(f"Created production line node: {self.name}")

        production_rate = await self.node.add_variable(
            self._idx, "ProductionRate", self._production_rate
        )
        await production_rate.set_writable()
        efficiency = await self.node.add_variable(
            self._idx, "Efficiency", self._efficiency
        )
        await efficiency.set_writable()

        batch_id = await self.node.add_property(self._idx, "BatchId", self._batch_id)
        await batch_id.set_writable()
        return self.node

    async def add_equipment(self, equipment: Equipment):
        """Add equipment to the production line"""
        await self.node.add_reference(equipment.node, ua.ObjectIds.HasComponent)

    def __str__(self):
        return f"ProductionLine(name={self.name})"

    async def run_simulation(self):
        """Run the simulation of the production line"""
        tasks = [
            asyncio.create_task(self._set_production_rate()),
            asyncio.create_task(self._set_efficiency()),
        ]
        await asyncio.gather(*tasks)

    async def _set_production_rate(self):
        """Set the production rate of the production line"""
        while True:
            self._production_rate = self._production_rate * random.uniform(0.5, 1.5)
            self._logger.info(
                f"Production rate set to {self._production_rate} for {self.name}"
            )
            await asyncio.sleep(3)

    async def _set_efficiency(self):
        """Set the efficiency of the production line"""
        while True:
            self._efficiency = self._efficiency * random.uniform(0.5, 1.5)
            self._logger.info(f"Efficiency set to {self._efficiency} for {self.name}")
            await asyncio.sleep(3)
