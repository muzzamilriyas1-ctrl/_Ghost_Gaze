import datetime

def log_threat(log_file):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{now}] Stranger detected!\n")