#!/bin/bash
# Backup diaper tracker database
# Add to crontab: 0 2 * * * /opt/diaper-tracker/backup_db.sh

BACKUP_DIR="/opt/diaper-tracker/backups"
DB_PATH="/opt/diaper-tracker/database.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
cp "$DB_PATH" "$BACKUP_DIR/database_${DATE}.db"

# Keep only last 30 backups
ls -t "$BACKUP_DIR"/database_*.db | tail -n +31 | xargs -r rm
