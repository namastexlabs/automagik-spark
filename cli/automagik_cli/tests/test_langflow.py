import asyncio
import pytest
from automagik_cli.langflow_client import LangflowClient, FlowBuilder

@pytest.mark.asyncio
async def test_flow_execution():
    """Test running a flow with specific configuration."""
    client = LangflowClient()
    
    # Build flow configuration for audio to message automation
    builder = FlowBuilder()
    
    # Add components with minimal configuration (empty tweaks)
    components = [
        "CustomComponent-88JDQ",
        "CustomComponent-8IQeG",
        "CurrentDate-BKLgt",
        "CustomComponent-QYtaC",
        "ParseData-Vfknv",
        "ChatOutput-0cetX",
        "ChatInput-fiBS9"
    ]
    
    for component_id in components:
        builder.add_component(component_id, component_id.split('-')[0])
    
    # Run the flow with the configured components
    result = await client.run_flow(
        flow_name="audio_to_messages_1d",
        input_value="message",
        input_type="chat",
        output_type="chat",
        tweaks=builder.get_tweaks(),
        stream=False
    )
    
    assert result is not None
    assert "session_id" in result
    assert "outputs" in result
    
    print("\nFlow execution result:", result)

@pytest.mark.asyncio
async def test_flow_execution_with_full_config():
    """Test running a flow with full component configuration."""
    client = LangflowClient()
    
    # Build flow configuration
    builder = FlowBuilder()
    
    # Add components with their full configurations
    builder.add_component(
        "CustomComponent-88JDQ", 
        "CustomComponent",
        api_key="audio_trans",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        instance_id="felipe_evo_instance",
        language="",
        server_url="http://192.168.112.131:4040",
        transcription_delay=1500
    )
    
    builder.add_component(
        "CustomComponent-8IQeG",
        "CustomComponent",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        instance_id="felipe_evo_instance",
        page=1,
        page_size=100,
        sort_direction="DESC"
    )
    
    builder.add_component(
        "CurrentDate-BKLgt",
        "CurrentDate",
        interval="1 day",
        timezone="America/Sao_Paulo"
    )
    
    builder.add_component(
        "CustomComponent-QYtaC",
        "CustomComponent",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        query="SELECT * FROM pg_stat_activity;"
    )
    
    builder.add_component(
        "ParseData-Vfknv",
        "ParseData",
        sep="\n",
        template="SELECT pg_terminate_backend(pid) FROM pg_stat_activity  WHERE datname = 'evolution_db'   AND state = 'idle'   AND pid <> pg_backend_pid();"
    )
    
    builder.add_component(
        "ChatOutput-0cetX",
        "ChatOutput",
        sender="Machine",
        sender_name="AI",
        should_store_message=True,
        data_template="{text}"
    )
    
    builder.add_component(
        "ChatInput-fiBS9",
        "ChatInput",
        sender="User",
        sender_name="User",
        should_store_message=False
    )
    
    # Run the flow with the configured components
    result = await client.run_flow(
        flow_name="audio_to_messages_1d",
        input_value="message",
        input_type="chat",
        output_type="chat",
        tweaks=builder.get_tweaks(),
        stream=False
    )
    
    assert result is not None
    assert "session_id" in result
    assert "outputs" in result
    
    print("\nFlow execution result with full config:", result)

if __name__ == "__main__":
    asyncio.run(test_flow_execution())
    asyncio.run(test_flow_execution_with_full_config())
