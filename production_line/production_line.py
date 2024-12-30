import logging
from typing import Optional
from production_line.equipment import Equipment
from asyncua import Node, ua, Client
import asyncio
from asyncio import Task
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

    _batch_id: Optional[Node] = None
    _production_rate: Optional[Node] = None
    _efficiency: Optional[Node] = None
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

    def __str__(self):
        return f"ProductionLine(name={self.name})"

    async def initialize(self):
        """Create a node object for the production line"""
        self.node = await self._parent_node.add_object(self._idx, self.name)
        self._logger.info(f"Created production line node: {self.name}")

        # Create ProductionRate variable
        self._production_rate = await self.node.add_variable(
            self._idx, "ProductionRate", 0.0, ua.VariantType.Double
        )
        await self._production_rate.set_writable()

        # Create Efficiency variable
        self._efficiency = await self.node.add_variable(
            self._idx, "Efficiency", 0.0, ua.VariantType.Double
        )
        await self._efficiency.set_writable()

        # Create BatchId property
        self._batch_id = await self.node.add_property(
            self._idx, "BatchId", "", ua.VariantType.String
        )
        await self._batch_id.set_writable()

        return self.node

    async def add_equipment(self, equipment: Equipment):
        """Add equipment to the production line"""
        await self.node.add_reference(equipment.node, ua.ObjectIds.HasComponent)

    async def start_batch(self, batch_id: str):
        await self._batch_id.write_value(batch_id)
        await self._production_rate.write_value(0.7)
        await self._efficiency.write_value(0.5)

    async def stop_batch(self):
        await self._batch_id.write_value("")
        await self._production_rate.write_value(0.0)
        await self._efficiency.write_value(0.0)

    async def run_simulation(self) -> list[Task]:
        await self.start_batch("batch-12")
        """Run the simulation of the production line"""
        tasks = [
            asyncio.create_task(self._set_production_rate()),
            asyncio.create_task(self._set_efficiency()),
        ]
        return tasks

    async def _set_production_rate(self):
        """Set the production rate of the production line"""
        while True:
            production_rate = await self._production_rate.read_value()
            await self._production_rate.set_value(
                round(production_rate * random.uniform(0.5, 1.0), 4)
            )
            self._logger.info(
                f"Production rate set to {production_rate} for {self.name}"
            )
            await asyncio.sleep(1)

    async def _set_efficiency(self):
        """Set the efficiency of the production line"""
        while True:
            efficiency = await self._efficiency.read_value()
            await self._efficiency.set_value(
                round(efficiency * random.uniform(0.5, 1.0), 4)
            )
            self._logger.info(f"Efficiency set to {efficiency} for {self.name}")
            await asyncio.sleep(1)
