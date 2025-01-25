# TODO

## High Priority

-   **Implement One-Time Schedules:**
    -   Add support for schedules that run only once at a specified date and time.
    -   This will allow users to schedule individual tasks for execution without recurrence.
    -   Update the `SchedulerService` to handle this new schedule type.
    -   Update the CLI and API to allow creating and managing one-time schedules.

-   **Implement Schedule Management:**
    -   Add functionality to create new schedules.
    -   Allow editing of existing schedules (e.g., update the schedule expression, flow parameters, status).
    -   Implement the ability to pause/resume schedules.
    -   Provide options to delete schedules.
    -   Ensure proper error handling and validation.

-   **Testing for New Features:**
    -   Create comprehensive test cases for:
        -   One-time schedules (creation, execution, edge cases)
        -   Schedule management (creation, editing, deletion, pausing/resuming)
    -   Integrate these tests into the existing test suite.

## Medium Priority

-   **Fix Integration Tests:**
    -   Investigate and resolve the failing integration tests.
    -   Specifically, address the issues related to flow syncing and data validation.
    -   Update mock data and assertions to match the actual API response format and database interactions.

## Nice to Have Early On

-   **Security Audit:**
    -   Conduct a thorough security audit of the codebase.
    -   Identify and address any potential vulnerabilities.
    -   Pay special attention to API authentication, data validation, and error handling.

## Nice to Have

-   **Performance Optimization:**
    -   Profile the application to identify performance bottlenecks.
    -   Optimize database queries and API response times.
    -   Consider caching mechanisms for frequently accessed data.

-   **Improve Error Handling:**
    -   Add more specific exception types for different error scenarios.
    -   Provide more informative error messages to users and in logs.
    -   Implement a robust error reporting mechanism.

-   *Expand API Functionality:**
    -   Add more API endpoints for managing flows, schedules, and tasks.
    -   Implement filtering, sorting, and pagination for list endpoints.

-   **Enhance Task Runner:**
    -   Add support for task dependencies.
    -   Implement more sophisticated retry mechanisms.
    -   Improve task status and progress tracking.

-   **Add More Documentation*:**
    -   Expand the documentation with more examples, use cases, and troubleshooting tips.
    -   Improve the API documentation with detailed request/response schemas.