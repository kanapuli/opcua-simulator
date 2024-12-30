from asyncua import Node
import logging
from .quality_control import QualityControl


async def get_milk_quality_control(
    parent_node: Node,
    idx: int,
    logger: logging.Logger,
) -> QualityControl:
    """
    Creates a milk quality control system
    """
    quality_control = QualityControl(
        name="Milk Quality Control",
        logger=logger,
        parent_node=parent_node,
        idx=idx,
    )
    await quality_control.initialize()
    return quality_control
