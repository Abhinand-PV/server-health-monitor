#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Load environment variables from .env file
set -a
source .env
set +a

# Run the health check script
python3 health_check.py

# Push logs to GitHub
git add logs/health_log.txt
git commit -m "Health check log update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
