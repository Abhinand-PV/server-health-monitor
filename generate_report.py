import os
import re
from datetime import datetime, timedelta

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "health_log.txt")
REPORT_FILE = os.path.join(LOG_DIR, "daily_report.txt")


def parse_log_entries():
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return []

    entries = []
    with open(LOG_FILE, "r") as f:
        content = f.read()

    pattern = (
        r"Health Check - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\n"
        r"={50}\n"
        r"CPU Usage:\s+([\d.]+)%\n"
        r"Memory Usage:\s+([\d.]+)%\n"
        r"Disk Usage:\s+([\d.]+)%"
    )

    for match in re.finditer(pattern, content):
        timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        entries.append({
            "timestamp": timestamp,
            "cpu": float(match.group(2)),
            "memory": float(match.group(3)),
            "disk": float(match.group(4)),
        })

    return entries

def generate_report():
    entries = parse_log_entries()

    if not entries:
        print("No entries to report on.")
        return

    cutoff = datetime.now() - timedelta(hours=24)
    recent = [e for e in entries if e["timestamp"] > cutoff]

    if not recent:
        print("No entries in the last 24 hours.")
        return

    avg_cpu = sum(e["cpu"] for e in recent) / len(recent)
    avg_memory = sum(e["memory"] for e in recent) / len(recent)
    peak_cpu = max(e["cpu"] for e in recent)
    peak_memory = max(e["memory"] for e in recent)
    disk_start = recent[0]["disk"]
    disk_end = recent[-1]["disk"]
    disk_trend = disk_end - disk_start

    report = (
        f"\n{'='*50}\n"
        f"Daily Health Summary - {datetime.now().strftime('%Y-%m-%d')}\n"
        f"{'='*50}\n"
        f"Period: Last 24 hours ({len(recent)} checks)\n"
        f"\n"
        f"CPU:\n"
        f"  Average: {avg_cpu:.1f}%\n"
        f"  Peak:    {peak_cpu:.1f}%\n"
        f"\n"
        f"Memory:\n"
        f"  Average: {avg_memory:.1f}%\n"
        f"  Peak:    {peak_memory:.1f}%\n"
        f"\n"
        f"Disk:\n"
        f"  Current: {disk_end:.1f}%\n"
        f"  Trend:   {'+' if disk_trend >= 0 else ''}{disk_trend:.1f}%\n"
        f"{'='*50}\n"
    )

    with open(REPORT_FILE, "a") as f:
        f.write(report)

    print(report)


if __name__ == "__main__":
    generate_report()

