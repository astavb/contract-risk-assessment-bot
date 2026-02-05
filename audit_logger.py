import json, os
from datetime import datetime

def log_audit(data):
    os.makedirs("audit_logs", exist_ok=True)
    path = f"audit_logs/audit_{int(datetime.now().timestamp())}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path
