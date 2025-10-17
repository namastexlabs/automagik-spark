#!/usr/bin/env python3
"""Script to sync Hive workflows into Spark database."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automagik_spark.core.database.session import get_async_session
from automagik_spark.core.database.models import Workflow, Source, SourceType
from automagik_spark.core.workflows.automagik_hive import AutomagikHiveManager
from sqlalchemy import select


async def sync_hive_workflows():
    """Sync all workflows from Hive to Spark database."""

    # Configuration
    hive_url = "http://localhost:8886"
    hive_api_key = "your_api_key_here"  # Will be read from source

    async with get_async_session() as session:
        print("🔍 Looking for Hive source in database...")

        # Get or create Hive source
        result = await session.execute(
            select(Source).where(
                Source.source_type == SourceType.AUTOMAGIK_HIVE,
                Source.url == hive_url
            )
        )
        source = result.scalar_one_or_none()

        if not source:
            print("❌ No Hive source found in database. Creating one...")
            source = Source(
                source_type=SourceType.AUTOMAGIK_HIVE,
                name="AutoMagik Hive",
                url=hive_url,
                api_key="test_key",  # Replace with actual key if needed
                config={}
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)
            print(f"✅ Created Hive source: {source.id}")
        else:
            print(f"✅ Found Hive source: {source.id}")

        # Initialize Hive manager
        hive_manager = AutomagikHiveManager(
            api_url=source.url,
            api_key=source.api_key,
            source_id=source.id
        )

        # List all flows from Hive
        print("\n📥 Fetching flows from Hive...")
        flows = hive_manager.list_flows_sync()
        print(f"Found {len(flows)} flows in Hive")

        # Sync each flow
        synced = 0
        for flow in flows:
            flow_id = flow['id']
            flow_name = flow['name']
            flow_type = flow['data']['type']

            # Check if workflow already exists
            result = await session.execute(
                select(Workflow).where(
                    Workflow.flow_id == flow_id,
                    Workflow.source_id == source.id
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  ⏭️  Skipping {flow_name} ({flow_type}) - already synced")
                continue

            # Create new workflow
            workflow = Workflow(
                flow_id=flow_id,
                name=flow_name,
                description=flow.get('description', ''),
                source_id=source.id,
                source_data=flow,
                input_component="message",  # Default for Hive flows
                output_component="result"  # Default for Hive flows
            )
            session.add(workflow)
            synced += 1
            print(f"  ✅ Synced {flow_name} ({flow_type})")

        # Commit all changes
        await session.commit()
        print(f"\n🎉 Successfully synced {synced} new workflows from Hive!")

        # List all workflows
        result = await session.execute(select(Workflow))
        workflows = result.scalars().all()
        print(f"\n📊 Total workflows in database: {len(workflows)}")
        for wf in workflows:
            print(f"  - {wf.name} (ID: {wf.flow_id})")


if __name__ == "__main__":
    asyncio.run(sync_hive_workflows())
