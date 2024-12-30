from asyncua import Node, ua
import logging
import random
from typing import Optional


class QualityControl:
    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        parent_node: Node,
        idx: int,
    ):
        self.name = name
        self.logger = logger
        self.parent_node = parent_node
        self.idx = idx
        self.node: Optional[Node] = None

    async def initialize(self) -> Node:
        """Initialize the quality control system with its variables and methods"""
        self.node = await self.parent_node.add_object(
            self.idx, self.name, objecttype=None
        )

        # Add variables with correct variant types
        self.ph_level = await self.node.add_variable(
            self.idx,
            "pH Level",
            ua.Variant(6.5, ua.VariantType.Double),  # Use Double for floating point
        )
        await self.ph_level.set_writable()

        self.fat_content = await self.node.add_variable(
            self.idx,
            "Fat Content",
            ua.Variant(3.0, ua.VariantType.Double),  # Use Double for floating point
        )
        await self.fat_content.set_writable()

        self.bacterial_count = await self.node.add_variable(
            self.idx,
            "Bacterial Count",
            ua.Variant(1000, ua.VariantType.Int64),  # Use Int64 for integers
        )
        await self.bacterial_count.set_writable()

        # Add methods
        await self.node.add_method(
            self.idx, "RunTest", self.run_test, [], [ua.VariantType.Boolean]
        )

        await self.node.add_method(
            self.idx,
            "GenerateReport",
            self.generate_report,
            [],
            [ua.VariantType.String],
        )

        self.logger.info(f"Initialized {self.name}")
        return self.node

    async def run_test(self, parent: Node) -> bool:
        """Run quality control tests and update variables"""
        # Simulate random test values with correct variant types
        await self.ph_level.write_value(
            ua.Variant(random.uniform(6.5, 6.8), ua.VariantType.Double)
        )
        await self.fat_content.write_value(
            ua.Variant(random.uniform(3.0, 5.0), ua.VariantType.Double)
        )

        # Simulate bacterial count decrease
        current_count = await self.bacterial_count.read_value()
        new_count = max(0, int(current_count * 0.8))  # Decrease by 20%
        await self.bacterial_count.write_value(
            ua.Variant(new_count, ua.VariantType.Int64)
        )

        self.logger.info(f"Quality control test run completed for {self.name}")
        return True

    async def generate_report(self, parent: Node) -> str:
        """Generate a quality control report"""
        ph = await self.ph_level.read_value()
        fat = await self.fat_content.read_value()
        bacteria = await self.bacterial_count.read_value()

        report = (
            f"Quality Control Report\n"
            f"-------------------\n"
            f"pH Level: {ph:.2f}\n"
            f"Fat Content: {fat:.1f}%\n"
            f"Bacterial Count: {bacteria}\n"
            f"Status: {'PASS' if self.is_quality_acceptable(ph, fat, bacteria) else 'FAIL'}"
        )

        self.logger.info(f"Generated quality report for {self.name}")
        return report

    def is_quality_acceptable(self, ph: float, fat: float, bacteria: int) -> bool:
        """Check if quality parameters are within acceptable ranges"""
        return 6.5 <= ph <= 6.8 and 3.0 <= fat <= 5.0 and bacteria < 1000
