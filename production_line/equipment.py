import logging
from typing import Callable

from asyncua import Node


class Equipment:
    """Equipment for a production line"""

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

        for property in self.properties:
            for prop_name, prop_value in property.items():
                prop = await self.node.add_property(self.idx, prop_name, prop_value)
                await prop.set_writable()

        for method in self.methods:
            for method_name, method_func in method.items():
                await self.node.add_method(self.idx, method_name, method_func)
