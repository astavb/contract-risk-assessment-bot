import json
import os
from datetime import datetime


def save_audit_log(data: dict) -> str:
    """
    Saves an audit log locally as JSON.
    Used for confidentiality & traceability.
    """

    os.makedirs("audit_logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"audit_logs/audit_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path
