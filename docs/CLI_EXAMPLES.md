
# Automagik-Spark CLI Examples

This guide provides practical examples for using the `automagik-spark` CLI to manage and schedule your workflows.
# Prerequisites & Setup

# Prerequisites & Setup

Before using the CLI, make sure you have run the development setup script:

```bash
# Make the script executable (if needed)
chmod +x ./scripts/setup_dev.sh

# Run the dev setup (Mac/Linux)
./scripts/setup_dev.sh


# Windows PowerShell (if provided)
# ./scripts/setup_dev.ps1


## Getting Started

1)First, ensure `automagik-spark` is installed and accessible. You can verify this with the `--help` command.

```bash
automagik-spark --help

Expected Output:
Options:
  --debug / --no-debug
  --no-telemetry        Disable telemetry for this session
  --help                Show this message and exit.

Commands:
  api        API server commands
  db         Database management commands
  schedules  Manage workflow schedules.
  sources    Manage workflow sources.
  tasks      Manage workflow tasks.
  telemetry  Manage telemetry settings.
  worker     Worker management commands
  workflows  Workflow management commands



Subcommand Usage Clarification

In automagik-spark, all CLI actions are run through the main command, followed by a subcommand.
❌ Incorrect usage
api
db
schedules


This will fail because the shell cannot find standalone commands named api, db, or schedules.

✅ Correct usage

automagik-spark api --help
automagik-spark db migrate
automagik-spark schedules list
automagik-spark sources add --name my-langflow --type langflow --url http://localhost:7860


The general pattern is:
automagik-spark <subcommand> [options]



## Troubleshooting

Here are solutions to common issues you might encounter during setup.

### `zsh: command not found: automagik-spark`

If you get this error, try these steps in order:

1.  **Activate Virtual Environment:** Make sure your prompt starts with `(venv)`. If not, run:
    ```bash
    source venv/bin/activate
    ```
2.  **Install the Package:** The command must be installed inside your active environment.
    ```bash
    pip install -e .
    ```
3.  **Refresh Your Shell (for zsh users):** If you just installed the package, your shell might not have found it yet.
    ```bash
    rehash
    ```

### `PermissionError: [Errno 13] Permission denied`

This happens if the app can't write to its log directory at `/var/log/automagik`.

1.  **Create the directory with admin rights:**
    ```bash
    sudo mkdir -p /var/log/automagik
    ```
2.  **Give your user ownership:**
    ```bash
    sudo chown $(whoami) /var/log/automagik
    ```

### `ERROR: Package ... requires a different Python`

This means your virtual environment was created with an incompatible Python version. You must create it with the correct one (e.g., Python 3.12 or newer).

```bash
# Deactivate and remove the old venv first
deactivate
rm -rf venv

# Create the new venv with the correct python version
python3.12 -m venv venv



2️⃣ Add a Workflow Source (LangFlow Example)
automagik-spark sources add \
  --name my-langflow \
  --type langflow \
  --url http://localhost:7860 \
  --api-key API_KEY_123


✅ Success:

Source added successfully: my-langflow


❌ Errors: check greenlet, DB connection, or URL format.

3️⃣ List Available Workflows
automagik-spark workflow list


Example output:

Available Workflows:
1. daily-report
2. weekly-backup
3. ai-health-monitor

4️⃣ Create Workflow Schedules
(a) Interval Schedule
automagik-spark schedule create daily-report --interval "10m"


Output:

Schedule created: runs every 10 minutes

(b) Cron Schedule
automagik-spark schedule create backup-flow "0 2 * * 0"


Output:

Schedule created: runs every Sunday at 2 AM

(c) One-Time Schedule
automagik-spark schedule create product-launch --once "2025-11-01T09:00:00Z"


Output:

One-time schedule set for 2025-11-01T09:00:00Z

5️⃣ Monitor Schedules & Tasks
List Schedules
automagik-spark schedule list


Example output:

Workflow         | Type   | Next Run               | Status
-----------------|--------|-----------------------|--------
daily-report     | Cron   | 2025-10-27 08:00:00   | Active
backup-flow      | Cron   | 2025-10-26 02:00:00   | Active

Show Schedule Details
automagik-spark schedule show daily-report


Output:

Workflow: daily-report
Type: Cron
Expression: 0 8 * * 1-5
Next Run: 2025-10-27 08:00:00
Status: Active

List Task Execution History
automagik-spark task list --limit 10


Output:

ID    | Workflow       | Status   | Started             | Duration
------|----------------|----------|--------------------|---------
12345 | daily-report   | Success  | 2025-10-24 08:00:00| 2.3s
12346 | backup-flow    | Failed   | 2025-10-24 02:00:00| 0.8s

6️⃣ Telemetry (Optional)

Enabled by default. Disable:

# Mac/Linux
export AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true

# Windows PowerShell
setx AUTOMAGIK_SPARK_DISABLE_TELEMETRY true

7️⃣ Common Cron Patterns
Description	Expression
Every 5 minutes	*/5 * * * *
Every hour	0 * * * *
Every day at midnight	0 0 * * *
Weekdays at 9 AM	0 9 * * 1-5
Sundays at 2 AM	0 2 * * 0
First day of month	0 0 1 * *

8️⃣ Troubleshooting (Cross-Platform)
Symptom	Cause	Fix
automagik-spark: command not found	Venv not active / not installed	Activate venv + pip install -e .
greenlet missing	Missing dependency	pip install greenlet
DB connection failed	Postgres not running, wrong port, db missing	Start DB, ensure DB exists, check .env DATABASE_URL
Redis/Celery fail	Redis not running	Start Redis (redis-server) on configured port
Invalid URL	Bad workflow source URL	Must start with http:// or https://



------


Full CLI Workflow Example (Cross-Platform)
# ============================================================
# 1️⃣ Activate Virtual Environment
# ============================================================

# Mac/Linux
source venv/bin/activate

# Windows PowerShell
# .\venv\Scripts\Activate.ps1

# Upgrade pip (optional, recommended)
python -m pip install --upgrade pip

# Install Automagik Spark if not installed
pip install -e .

# ============================================================
# 2️⃣ Verify Installation
# ============================================================

automagik-spark --help
# ✅ Should display available commands: api, db, sources, schedules, tasks, worker, workflows, telemetry

# ============================================================
# 3️⃣ Add a LangFlow Workflow Source
# ============================================================

automagik-spark sources add \
  --name my-langflow \
  --type langflow \
  --url http://localhost:7860 \
  --api-key API_KEY_123

# ✅ Expected output:
# Source added successfully: my-langflow

# Troubleshooting:
# - If you see "greenlet missing", run: pip install greenlet
# - If DB connection fails, check your .env DATABASE_URL and make sure Postgres is running

# ============================================================
# 4️⃣ List Available Workflows from Sources
# ============================================================

automagik-spark workflow list
# Example output:
# Available Workflows:
# 1. daily-report
# 2. weekly-backup
# 3. ai-health-monitor

# ============================================================
# 5️⃣ Create Workflow Schedules
# ============================================================

# (a) Interval schedule: run daily-report every 10 minutes
automagik-spark schedule create daily-report --interval "10m"

# (b) Cron schedule: run backup-flow every Sunday at 2 AM
automagik-spark schedule create backup-flow "0 2 * * 0"

# (c) One-time schedule: run product-launch once at 2025-11-01 09:00 UTC
automagik-spark schedule create product-launch --once "2025-11-01T09:00:00Z"

# ✅ Expected outputs:
# Schedule created: runs every 10 minutes
# Schedule created: runs every Sunday at 2 AM
# One-time schedule set for 2025-11-01T09:00:00Z

# ============================================================
# 6️⃣ List All Schedules
# ============================================================

automagik-spark schedule list
# Example output:
# Workflow         | Type   | Next Run               | Status
# -----------------|--------|-----------------------|--------
# daily-report     | Interval | 2025-10-25 08:00:00 | Active
# backup-flow      | Cron     | 2025-10-26 02:00:00 | Active
# product-launch   | One-Time | 2025-11-01 09:00:00 | Active

# ============================================================
# 7️⃣ Show Schedule Details
# ============================================================

automagik-spark schedule show daily-report
# Example output:
# Workflow: daily-report
# Type: Interval
# Interval: 10 minutes
# Next Run: 2025-10-25 08:00:00
# Status: Active

# ============================================================
# 8️⃣ List Recent Task Executions
# ============================================================

automagik-spark task list --limit 10
# Example output:
# ID    | Workflow       | Status   | Started             | Duration
# ------|----------------|----------|--------------------|---------
# 12345 | daily-report   | Success  | 2025-10-24 08:00:00| 2.3s
# 12346 | backup-flow    | Failed   | 2025-10-24 02:00:00| 0.8s

# ============================================================
# ✅ 9️⃣ Optional: Disable Telemetry
# ============================================================

# Mac/Linux
export AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true

# Windows PowerShell
setx AUTOMAGIK_SPARK_DISABLE_TELEMETRY true