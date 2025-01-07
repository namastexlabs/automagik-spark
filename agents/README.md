# Agents

This module manages the creation and management of agents that are bound to Langflow flows.

## Features

- Create agents bound to specific flows
- Map input/output components for each agent
- Manage agent lifecycle (activate/deactivate)

## Structure

- `models.py`: Database models for agents
- `cli/`: Command-line interface scripts
  - `list.py`: List available agents
  - `create.py`: Create new agents
  - `update.py`: Update existing agents
  - `delete.py`: Delete agents
