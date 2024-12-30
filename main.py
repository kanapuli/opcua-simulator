import asyncio
import logging

from asyncio import Task
from asyncua import Server
from enterprise import Enterprise
from asyncua.common.methods import uamethod
from milk_processor import get_milk_processing_line
from production_line.production_line import ProductionLine


async def main():
    _logger = logging.getLogger(__name__)
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server")

    uri = "https://kanapuli.github.io/dairy-enterprise"
    idx = await server.register_namespace(uri)

    simulation_tasks: list[Task] = []
    async with server:
        _logger.info("Starting OPC UA server...")
        dairy_enterprise = await Enterprise.create(
            name="Dairy Enterprise",
            logger=_logger,
            server=server,
            idx=idx,
            production_lines=[],
        )
        _logger.info(f"Created {dairy_enterprise}")
        # Start the simulation for enterprise variables
        simulation_tasks.extend(await dairy_enterprise.run_simulation())

        milk_processing_line = await get_milk_processing_line(
            dairy_enterprise.node, idx, _logger
        )
        # Collect tasks from milk processing line
        milk_line_tasks = await milk_processing_line.run_simulation()
        simulation_tasks.extend(milk_line_tasks)

        # Initialize other production lines...
        icecrean_production_line = ProductionLine(
            name="Icecrean Production Line",
            logger=_logger,
            parent_node=dairy_enterprise.node,
            idx=idx,
        )
        await icecrean_production_line.initialize()

        cheese_production_line = ProductionLine(
            name="Cheese Production Line",
            logger=_logger,
            parent_node=dairy_enterprise.node,
            idx=idx,
        )
        await cheese_production_line.initialize()
        cheese_line_tasks = await cheese_production_line.run_simulation()
        simulation_tasks.extend(cheese_line_tasks)

        yogurt_production_line = ProductionLine(
            name="Yogurt Production Line",
            logger=_logger,
            parent_node=dairy_enterprise.node,
            idx=idx,
        )
        await yogurt_production_line.initialize()

        await dairy_enterprise.add_production_line(cheese_production_line)
        await dairy_enterprise.add_production_line(yogurt_production_line)
        await dairy_enterprise.add_production_line(icecrean_production_line)

        # Ensure all tasks are valid before gathering
        valid_tasks = [
            task for task in simulation_tasks if isinstance(task, asyncio.Task)
        ]

        try:
            # Then gather them
            await asyncio.gather(*valid_tasks)
        except Exception as e:
            _logger.error(f"Error during simulation: {e}")
            # Cancel any remaining tasks
            for task in valid_tasks:
                if not task.done():
                    task.cancel()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=True)
