#!/bin/bash
# Script to fix WorkflowSync imports in workflow_tasks.py

TARGET_FILE="/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks.py"
BACKUP_FILE="${TARGET_FILE}.backup"

echo "Creating backup of $TARGET_FILE"
cp "$TARGET_FILE" "$BACKUP_FILE"

echo "Applying fixes to $TARGET_FILE"
sed -i 's/from \.\.\.core\.workflows\.sync import WorkflowSync/from ...core.workflows.sync import WorkflowSyncSync/g' "$TARGET_FILE"
sed -i 's/with WorkflowSync(session) as sync:/with WorkflowSyncSync(session) as sync:/g' "$TARGET_FILE"

echo "Verifying changes:"
grep -n "WorkflowSync" "$TARGET_FILE"

echo "Done! Backup saved as $BACKUP_FILE"