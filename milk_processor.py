from production_line.equipements.pasteurizer import Pasteurizer
from production_line.equipements.homogenizer import Homogenizer
from production_line.production_line import ProductionLine
import logging
from asyncua import Node


async def get_pastuerizer(parent_node: Node, idx: int):
    """
    creates a pasteurizer

    Args:
        server (Server): The server to create the pasteurizer on
        idx (int): The index of the pasteurizer
    """
    pasteurizer = Pasteurizer(
        logger=logging.getLogger(__name__),
        parent_node=parent_node,
        idx=idx,
        variables=[{"Temperature": 0.0}, {"FlowRate": 0.0}, {"Status": "Off"}],
        properties=[{"DeviceID": "1PASTEUR"}],
        methods=[
            {"StartHeater": lambda Status: "On"},
            {"StopHeater": lambda Status: "Off"},
        ],
    )
    await pasteurizer.initialize()
    return pasteurizer


async def get_homogenizer(parent_node: Node, idx: int):
    """
    creates a homogenizer

    Args:
        server (Server): The server to create the homogenizer on
        idx (int): The index of the homogenizer
    """
    homogenizer = Homogenizer(
        logger=logging.getLogger(__name__),
        parent_node=parent_node,
        idx=idx,
        variables=[{"Pressure": 0.0}, {"Status": "Off"}],
        properties=[{"DeviceID": "1HOMOGEN"}],
        methods=[
            {"StartHomogenizer": lambda Status: "On"},
            {"StopHomogenizer": lambda Status: "Off"},
        ],
    )
    await homogenizer.initialize()
    return homogenizer


async def get_milk_processing_line(
    parent_node: Node,
    idx: int,
    logger: logging.Logger,
):
    """
    creates a milk processing line
    """
    milk_processing_line = ProductionLine(
        name="Milk Processing Line",
        logger=logger,
        parent_node=parent_node,
        idx=idx,
    )
    milk_processing_line_node = await milk_processing_line.initialize()
    pasteurizer = await get_pastuerizer(milk_processing_line_node, idx)
    homogenizer = await get_homogenizer(milk_processing_line_node, idx)

    # Add the equipment simulation tasks to the production line
    milk_processing_line.add_simulation_task(pasteurizer.run_simulation())
    milk_processing_line.add_simulation_task(homogenizer.run_simulation())

    return milk_processing_line
