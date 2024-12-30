import asyncio
from asyncio import Task
import logging
from typing import Callable
from asyncua import Node, ua
import random


class Equipment:
    """Equipment for a production line"""

    _variable_nodes: list[Node] = []

    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
        variables: list[dict[str, any]] | None = None,
        properties: list[dict[str, any]] | None = None,
        methods: list[dict[str, Callable[[], any]]] | None = None,
    ):
        self.name = name
        self.logger = logger
        self.parent_node = parent_node
        self.idx = idx
        self.node: Node = None
        self.variables = variables
        self.properties = properties
        self.methods = methods

    async def initialize(self):
        """Initialize the equipment"""
        self.node = await self.parent_node.add_object(self.idx, self.name)
        self.logger.info(f"Created equipment node: {self.name}")

        for variable in self.variables:
            for var_name, var_value in variable.items():
                var = await self.node.add_variable(self.idx, var_name, var_value)
                await var.set_writable()
                self._variable_nodes.append(var)

        for property in self.properties:
            for prop_name, prop_value in property.items():
                prop = await self.node.add_property(self.idx, prop_name, prop_value)
                await prop.set_writable()

        for method in self.methods:
            for method_name, method_func in method.items():
                await self.node.add_method(self.idx, method_name, method_func)

    def run_simulation(self) -> list[Task]:
        """Run the simulation"""
        tasks = []
        for node in self._variable_nodes:
            task = asyncio.create_task(self._set_random_values(node))
            tasks.append(task)
        return tasks

    async def _set_random_values(self, node: Node):
        """Set random values for the variables"""
        while True:
            data_type = await node.read_data_type_as_variant_type()
            if data_type == ua.VariantType.Float:
                await node.write_value(round(random.uniform(0, 100), 4))
            elif data_type == ua.VariantType.Double:
                await node.write_value(round(random.uniform(0, 100), 4))
            elif data_type == ua.VariantType.Boolean:
                await node.write_value(random.choice([True, False]))
            elif data_type == ua.VariantType.Int32:
                await node.write_value(random.randint(50, 100))
            elif data_type == ua.VariantType.Int64:
                await node.write_value(random.randint(0, 50))
            elif data_type == ua.VariantType.Int16:
                await node.write_value(random.randint(0, 25))
            elif data_type == ua.VariantType.String:
                await node.write_value(random.choice(["On", "Off"]))
            await asyncio.sleep(2)
