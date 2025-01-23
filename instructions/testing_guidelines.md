# Testing Guidelines and Common Pitfalls

## Test Structure

### File Organization
- Keep test files organized by component/feature (e.g., `test_flows.py`, `test_run.py`)
- Use descriptive test class and function names that reflect what's being tested
- Group related tests within the same test class

### Test Dependencies
- Place shared fixtures in `conftest.py` files
- Use the closest `conftest.py` to the tests that need the fixtures
- Consider fixture scope (function, class, module, session) carefully

## Common Pitfalls

### 1. CLI Testing
- When testing Click commands:
  - Use `catch_exceptions=False` to see actual exceptions instead of Click's error handling
  - For error messages, check log records using `caplog` fixture instead of stdout/stderr
  - Verify both exit codes and error messages
  - Mock all external dependencies (DB, API clients, etc.)

### 2. Async Operations
- Be careful with async code in tests:
  - Use proper async fixtures and test functions
  - Handle RuntimeError exceptions from asyncio when testing daemon modes
  - Consider using `asyncio.run()` for running async code in sync tests

### 3. Database Interactions
- Always mock database sessions in tests
- Use transaction rollbacks in integration tests
- Be careful with session management and cleanup
- Ensure database state is clean between tests

### 4. Mocking
- Mock at the right level:
  - Mock external services and APIs
  - Mock database sessions
  - Don't mock the code under test
- Verify mock calls and arguments when behavior depends on them
- Use `side_effect` for complex mock behaviors or raising exceptions

### 5. UUID Handling
- Be careful with UUID validation:
  - Test both valid and invalid UUID formats
  - Mock UUID generation for predictable test results
  - Handle UUID-related exceptions properly

## Current Areas of Focus

### 1. Error Handling
- Ensure all error cases are properly tested
- Verify error messages are logged correctly
- Check that appropriate exit codes are returned
- Test boundary conditions and edge cases

### 2. Schedule Management
- Test all schedule types (cron, interval, oneshot)
- Verify schedule creation, deletion, and listing
- Test schedule parameter validation
- Ensure proper timezone handling

### 3. Flow Integration
- Test flow synchronization
- Verify flow parameter handling
- Test flow execution through schedules
- Handle flow-related errors properly

### 4. Task Runner
- Test task creation and execution
- Verify task status updates
- Test task error handling
- Ensure proper cleanup of task resources

## Best Practices

1. **Isolation**: Each test should be independent and not rely on the state from other tests

2. **Clarity**: Test names should clearly describe what's being tested and expected behavior

3. **Coverage**: Aim for comprehensive coverage but focus on critical paths and edge cases

4. **Maintenance**: Keep tests simple and maintainable, avoid test code duplication

5. **Documentation**: Document complex test setups and any non-obvious test requirements

## Adding New Tests

When adding new tests, consider:

1. **Dependencies**: What external services/components need to be mocked?

2. **Fixtures**: Can existing fixtures be reused? Should new fixtures be created?

3. **Error Cases**: What can go wrong? Are all error paths tested?

4. **Edge Cases**: What are the boundary conditions? Are they tested?

5. **Integration**: How does this component interact with others? Are these interactions tested?

Remember to run the full test suite after adding new tests to ensure no regressions were introduced.
