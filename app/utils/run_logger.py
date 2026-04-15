import json
import os
from datetime import datetime


class RunLogger:
    """
    Logs each agent run into a structured JSON file
    """

    def __init__(self):
        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = f"logs/run_{timestamp}.json"

        self.data = {
            "timestamp": timestamp,
            "steps": []
        }

    def log(self, step_name: str, payload: dict):
        """
        Add step log
        """

        self.data["steps"].append({
            "step": step_name,
            "data": payload
        })

    def save(self):
        """
        Save logs to file
        """

        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)