import psutil
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

# Load configuration from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT")
DISK_THRESHOLD = int(os.environ.get("DISK_THRESHOLD", "80"))

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "health_log.txt")


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    disk = psutil.disk_usage("/")
    return disk.percent


def get_running_services():
    services = []
    for proc in psutil.process_iter(["pid", "name", "status"]):
        try:
            if proc.info["status"] == psutil.STATUS_RUNNING:
                services.append(proc.info["name"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return list(set(services))[:20]

def write_log(cpu, memory, disk, services):
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"\n{'='*50}\n"
        f"Health Check - {timestamp}\n"
        f"{'='*50}\n"
        f"CPU Usage:    {cpu}%\n"
        f"Memory Usage: {memory}%\n"
        f"Disk Usage:   {disk}%\n"
        f"Running Services ({len(services)}): {', '.join(services[:10])}\n"
        f"{'='*50}\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(log_entry)

def send_alert(subject, body):
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_RECIPIENT]):
        print("Email configuration incomplete. Skipping alert.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ALERT_RECIPIENT
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Alert sent to {ALERT_RECIPIENT}")
    except Exception as e:
        print(f"Failed to send alert: {e}")


def main():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    services = get_running_services()

    write_log(cpu, memory, disk, services)

    if disk > DISK_THRESHOLD:
        subject = f"ALERT: Disk Usage at {disk}% (Threshold: {DISK_THRESHOLD}%)"
        body = (
            f"Disk usage has exceeded the configured threshold.\n\n"
            f"Current Disk Usage: {disk}%\n"
            f"Threshold: {DISK_THRESHOLD}%\n"
            f"CPU Usage: {cpu}%\n"
            f"Memory Usage: {memory}%\n"
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        send_alert(subject, body)


if __name__ == "__main__":
    main()
