import asyncio
from asyncio import Task
import logging
import random
from asyncua import Server, ua, Node
from production_line.production_line import ProductionLine
from storage import MilkStorageTank, ColdStorage
from asyncua.common.methods import uamethod
from typing import Optional
from quality_control.milk_quality_control import get_milk_quality_control


class Enterprise:
    """
    Represents an enterprise (a whole factory) with production lines and storage units
    """

    _instance = None
    _total_milk_processed: Optional[Node] = None
    _production_status: Optional[Node] = None

    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        server: Server,
        idx: int,
        production_lines: list[ProductionLine],
    ) -> None:
        # Initialize instance attributes
        self.name = name
        self._logger = logger
        self._server = server
        self._idx = idx
        self._initialized = False
        self._production_lines = production_lines
        self._milk_storage: Optional[MilkStorageTank] = None
        self._cold_storage: Optional[ColdStorage] = None
        self._quality_control = None

    @classmethod
    async def create(
        cls,
        name: str,
        logger: logging.Logger,
        server: Server,
        idx: int,
        production_lines: list[ProductionLine],
    ):
        if not cls._instance:
            # Create new instance
            cls._instance = cls(name, logger, server, idx, production_lines)
            # Perform async initialization
            await cls._instance._initialize()
            await cls._instance._initialize_storage()
            cls._instance._initialized = True
        return cls._instance

    async def _initialize_storage(self):
        """Initialize storage units"""
        # Create storage folder node
        storage_idx = self._idx + 1000
        storage_node = await self.node.add_object(storage_idx, "Storage")
        await self.node.add_reference(storage_node, ua.ObjectIds.Organizes)

        # Initialize milk storage tank
        self._milk_storage = MilkStorageTank(
            self._logger,
            storage_node,
            storage_idx,
        )
        await self._milk_storage.initialize()

        # Initialize cold storage
        self._cold_storage = ColdStorage(
            self._logger,
            storage_node,
            storage_idx,
        )
        await self._cold_storage.initialize()

        self._logger.info("Storage units initialized")

    async def _initialize(self):
        """Add the enterprise node to the OPC UA server"""

        objects = self._server.get_objects_node()
        model_view = await objects.add_folder(self._idx, "ModelView")
        # Add a folder to the server
        # server_object = self._server.nodes.server
        # model_view = await server_object.add_folder(self._idx, "ModelView")
        self.node = await model_view.add_object(self._idx, self.name)
        self._logger.info(f"Created enterprise node: {self.name}")

        # Initialize quality control
        quality_control_idx = (
            self._idx + 2000
        )  # Using 2000 to avoid conflicts with storage (1000)
        self._quality_control = await get_milk_quality_control(
            self.node,
            quality_control_idx,
            self._logger,
        )
        await self.node.add_reference(
            self._quality_control.node, ua.ObjectIds.Organizes
        )
        self._logger.info("Quality control system initialized")

        for production_line in self._production_lines:
            await self.node.add_reference(production_line.node, ua.ObjectIds.Organizes)

        self._total_milk_processed = await self.node.add_variable(
            self._idx, "TotalMilkProcessed", 0.0, ua.VariantType.Double
        )

        self._production_status = await self.node.add_variable(
            self._idx, "ProductionStatus", False, ua.VariantType.Boolean
        )

        await self.node.add_method(self._idx, "StartProduction", self._start_production)
        await self.node.add_method(self._idx, "StopProduction", self._stop_production)

    @uamethod
    async def _start_production(self):
        """Start the production"""
        await self._production_status.write_value(True)
        self._logger.info(f"Production started for {self.name}")

    @uamethod
    async def _stop_production(self):
        """Stop the production"""
        await self._production_status.write_value(False)
        self._logger.info(f"Production stopped for {self.name}")

    def __str__(self):
        """String representation of the enterprise"""
        return f"Enterprise(name={self.name})"

    async def add_production_line(self, production_line: ProductionLine):
        """Add a production line to the enterprise"""
        self._production_lines.append(production_line)
        await self.node.add_reference(production_line.node, ua.ObjectIds.Organizes)

    @property
    def production_lines(self) -> list[ProductionLine]:
        """Get the production lines"""
        return self._production_lines

    @property
    def milk_storage(self) -> Optional[MilkStorageTank]:
        """Get the milk storage tank"""
        return self._milk_storage

    @property
    def cold_storage(self) -> Optional[ColdStorage]:
        """Get the cold storage unit"""
        return self._cold_storage

    @property
    def quality_control(self):
        """Get the quality control system"""
        return self._quality_control

    async def run_simulation(self) -> list[Task]:
        """Run the simulation"""
        tasks = [
            asyncio.create_task(self._set_total_milk_processed()),
            asyncio.create_task(self._set_production_status()),
        ]
        return tasks

    async def _set_total_milk_processed(self):
        """Set the total milk processed"""
        while True:
            total_milk_processed = await self._total_milk_processed.read_value()
            await self._total_milk_processed.set_value(
                round(total_milk_processed + random.uniform(0, 1.5), 2)
            )
            self._logger.info(
                f"Total milk processed: {total_milk_processed} for {self.name}"
            )
            await asyncio.sleep(1)

    async def _set_production_status(self):
        """Set the production status"""
        await self._production_status.write_value(True)
        self._logger.info(f"Production status set to True for {self.name}")
