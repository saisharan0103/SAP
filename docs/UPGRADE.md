# Upgrade Procedure

Follow these steps to upgrade the SAP application:

1. **Backup the database** before making changes.
2. Pull the latest application code.
3. Run `db/setup_db.sh` to apply new schema changes.
4. Rebuild the Docker image or executable package.
5. Redeploy the application and verify functionality.
