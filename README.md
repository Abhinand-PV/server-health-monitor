# Server Health Monitor

An automated server health monitoring script that checks CPU, memory, disk usage, and running services. Logs results with timestamps, sends email alerts when disk usage exceeds a threshold, and pushes logs to GitHub automatically.

## Features

- Monitors CPU load, memory usage, disk usage, and running services
- Timestamped logging to track system health over time
- Email alerts via Gmail when disk usage exceeds configurable threshold
- Automatic log push to GitHub for version-controlled history
- Runs on a schedule via cron

## Requirements

- Linux (or WSL on Windows)
- Python 3.6+
- psutil library
- Git
- Gmail account with App Password

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/server-health-monitor.git
   cd server-health-monitor
   ```

2. Install psutil:
   ```bash
   pip3 install psutil
   ```

3. Create a `.env` file with your settings:
   ```
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   ALERT_RECIPIENT=recipient@gmail.com
   DISK_THRESHOLD=80
   ```

4. Make the shell script executable:
   ```bash
   chmod +x run_healthcheck.sh
   ```

5. Add to crontab for automatic execution:
   ```bash
   crontab -e
   # Add this line to run every hour:
   0 * * * * /path/to/run_healthcheck.sh
   ```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| EMAIL_ADDRESS | Gmail address for sending alerts | - |
| EMAIL_PASSWORD | Gmail App Password (16 characters) | - |
| ALERT_RECIPIENT | Email address to receive alerts | - |
| DISK_THRESHOLD | Disk usage percentage to trigger alert | 80 |

## Generating a Gmail App Password

1. Go to your Google Account > Security
2. Enable 2-Step Verification if not already enabled
3. Go to App Passwords (search "app password" in account settings)
4. Generate a new app password and copy the 16-character code
5. Use this code as your EMAIL_PASSWORD

## License

MIT

