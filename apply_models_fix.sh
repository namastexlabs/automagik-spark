#!/bin/bash

# Backup the original file
cp /home/cezar/automagik/automagik-spark/automagik_spark/api/models.py /home/cezar/automagik/automagik-spark/automagik_spark/api/models.py.backup

# Apply the fix
cd /home/cezar/automagik/automagik-spark
python3 complete_fix.py

echo "Fix applied successfully! Backup saved as models.py.backup"
