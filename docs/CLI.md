# AutoMagik CLI Guide

This guide covers the AutoMagik command-line interface tools and usage.

## Global Options

These options apply to all commands:

```bash
--help          Show help message
--debug         Enable debug logging
--config FILE   Use alternate config file
```

## Flow Management

### List Flows
```bash
automagik flows list
```

Options:
- `--folder NAME`: Filter by folder
- `--source NAME`: Filter by source
- `--format {table,json}`: Output format

### Sync Flows
```bash
automagik flows sync
```

Options:
- `--source NAME`: Source to sync from
- `--force`: Force sync even if unchanged

## Task Management

### List Tasks
```bash
automagik tasks list
```

Options:
- `--flow-id ID`: Filter by flow
- `--status STATUS`: Filter by status
- `--limit N`: Limit number of results

### View Task Output
```bash
automagik tasks output <task-id>
```

### View Task Logs
```bash
automagik tasks logs <task-id>
```

Options:
- `--follow`: Follow log output
- `--tail N`: Show last N lines

## Schedule Management

### Create Schedule
```bash
automagik schedules create <flow-name>
```

Options:
- `--type {cron,interval}`: Schedule type
- `--expr EXPR`: Schedule expression
- `--params JSON`: Flow parameters

### List Schedules
```bash
automagik schedules list
```

Options:
- `--flow-id ID`: Filter by flow
- `--status STATUS`: Filter by status

### Delete Schedule
```bash
automagik schedules delete <schedule-id>
```

## Service Management

### Install Service
```bash
automagik install-service
```

Options:
- `--user NAME`: Run service as user
- `--port PORT`: Service port

### Service Status
```bash
automagik service status
```

## Database Management

### Initialize Database
```bash
automagik db init
```

### Migrate Database
```bash
automagik db migrate
```

Options:
- `--revision REV`: Target revision
- `--sql`: Generate SQL

## Examples

1. Create a scheduled flow:
```bash
automagik schedules create "Daily Report" \
  --type cron \
  --expr "0 9 * * *" \
  --params '{"input": "daily report"}'
```

2. View recent task failures:
```bash
automagik tasks list \
  --status failed \
  --limit 10
```

3. Follow task logs:
```bash
automagik tasks logs abc123 --follow
```

## Environment Variables

The CLI respects these environment variables:

- `AUTOMAGIK_API_KEY`: API authentication key
- `AUTOMAGIK_CONFIG`: Config file location
- `AUTOMAGIK_DEBUG`: Enable debug logging
- `DATABASE_URL`: Database connection string

## Configuration File

The CLI can be configured via `~/.automagik/config.yaml`:

```yaml
api_key: your-api-key
database_url: postgresql://...
log_level: INFO
```

## Logging

CLI logs are written to:
- `~/.automagik/cli.log`: Command execution logs
- `~/.automagik/debug.log`: Debug logs (if enabled)

## Troubleshooting

Common CLI issues:

1. **Command Not Found**
   - Ensure virtual environment is activated
   - Check PATH includes .venv/bin

2. **Authentication Errors**
   - Verify AUTOMAGIK_API_KEY is set
   - Check API key in config file

3. **Database Errors**
   - Verify DATABASE_URL is correct
   - Check database connectivity
