import asyncio
import logging

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

        milk_processing_line = await get_milk_processing_line(
            dairy_enterprise.node, idx, _logger
        )
        await milk_processing_line.run_simulation()
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
        await cheese_production_line.run_simulation()

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
        await asyncio.sleep(1000)

    # pumpObject = await serverObject.add_object(idx, "Pump")
    # pumpStatus = await pumpObject.add_variable(idx, "PumpStatus", 0.0)
    # await pumpStatus.set_writable()
    # pumpSpeed = await pumpObject.add_variable(idx, "PumpSpeed", 0.0)
    # await pumpSpeed.set_writable()
    # pumpDirection = await pumpObject.add_variable(idx, "PumpDirection", 0.0)
    # await pumpDirection.set_writable()
    # pumpFlowRate = await pumpObject.add_variable(idx, "PumpFlowRate", 0.0)
    # await pumpFlowRate.set_writable()
    # pumpPressure = await pumpObject.add_variable(idx, "PumpPressure", 0.0)
    # await pumpPressure.set_writable()
    # pumpTemperature = await pumpObject.add_variable(idx, "PumpTemperature", 0.0)
    # await pumpTemperature.set_writable()
    # pumpVoltage = await pumpObject.add_variable(idx, "PumpVoltage", 0.0)
    # await pumpVoltage.set_writable()
    # pumpCurrent = await pumpObject.add_variable(idx, "PumpCurrent", 0.0)
    # await pumpCurrent.set_writable()
    # pumpPower = await pumpObject.add_variable(idx, "PumpPower", 0.0)
    # await pumpPower.set_writable()
    # await server.nodes.objects.add_method(
    #     ua.NodeId("ServerMethod", idx),
    #     ua.QualifiedName("ServerMethod", idx),
    #     func,
    #     [ua.VariantType.Int64],
    #     [ua.VariantType.Int64],
    # )
    # _logger.info("Starting server!")
    # async with server:
    #     pumpVariables = [
    #         pumpStatus,
    #         pumpSpeed,
    #         pumpDirection,
    #         pumpFlowRate,
    #         pumpPressure,
    #         pumpTemperature,
    #         pumpVoltage,
    #         pumpCurrent,
    #         pumpPower,
    #     ]
    #     tasks = [
    #         asyncio.create_task(update_variable(var, _logger)) for var in pumpVariables
    #     ]

    #     await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=True)
