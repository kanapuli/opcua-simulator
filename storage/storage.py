from asyncua import Node, ua
import logging
from typing import Optional, Dict, Any, List


class Storage:
    """Base class for storage units in the production line"""

    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
        variables: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[List[Dict[str, Any]]] = None,
    ):
        self.name = name
        self.logger = logger
        self.idx = idx
        self.parent_node = parent_node
        self.variables = variables or []
        self.properties = properties or []

    async def initialize(self):
        """Initialize the storage unit in the OPC UA server"""
        self.node = await self.parent_node.add_object(self.idx, self.name)
        # Add reference to the parent node
        await self.parent_node.add_reference(
            self.node, ua.ObjectIds.HasChild, forward=True
        )
        self.logger.info(f"Created storage node: {self.name}")

        for variable in self.variables:
            for var_name, var_value in variable.items():
                var = await self.node.add_variable(self.idx, var_name, var_value)
                await var.set_writable()

        for property in self.properties:
            for prop_name, prop_value in property.items():
                prop = await self.node.add_property(self.idx, prop_name, prop_value)
                await prop.set_writable()
