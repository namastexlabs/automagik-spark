# AutoMagik Architecture

## Core Services

### Flow Manager
- Handles flow synchronization and storage
- Supports both string and dict data formats from LangFlow API
- Extracts and stores input/output components
- Manages flow metadata and versioning

### Flow Analyzer
- Analyzes flow components and structure
- Identifies input and output nodes
- Extracts tweakable parameters
- Validates flow structure

### Schedule Manager
- Manages flow execution schedules
- Creates and updates schedules
- Handles schedule metadata
- Manages schedule execution state

## Database Models

### FlowDB
- Stores flow data and metadata
- Tracks flow versions and states
- Manages flow relationships

### FlowComponent
- Tracks flow components and their relationships
- Stores component configurations
- Maps input/output connections

### Schedule
- Manages execution schedules for flows
- Tracks schedule states and history
- Handles schedule metadata

## Testing Strategy

### Integration Tests
- Uses SQLite for ephemeral testing
- Mocks LangFlow API responses
- Tests flow sync and schedule creation
- Verifies database operations

### Unit Tests
- Tests individual components
- Validates core functionality
- Ensures data integrity

## Development Status

### Recent Updates
- Added integration testing with SQLite
- Improved flow sync handling
- Enhanced error handling
- Added comprehensive test coverage

### Current Focus
- Improving test reliability
- Enhancing flow sync
- Expanding test coverage

See [TODO.md](/TODO.md) for detailed task tracking.
