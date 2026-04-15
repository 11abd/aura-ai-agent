import json
import os
from datetime import datetime


class RunLogger:
    """
    Logs each agent run into a structured folder inside logs/.
    """

    def __init__(self):
        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join("logs", f"run_{timestamp}")
        os.makedirs(self.run_dir, exist_ok=True)
        self.file_path = os.path.join(self.run_dir, "run.json")

        self.data = {
            "timestamp": timestamp,
            "run_dir": self.run_dir,
            "steps": []
        }

    def log(self, step_name: str, payload: dict):
        """
        Add a structured step log.
        """

        self.data["steps"].append({
            "step": step_name,
            "data": payload
        })

    def save_artifact(self, name: str, content: str, extension: str = "txt"):
        """
        Save a text artifact inside the current run folder.
        """

        safe_name = "".join(
            char if char.isalnum() or char in ("-", "_") else "_"
            for char in name.strip()
        )
        artifact_path = os.path.join(self.run_dir, f"{safe_name}.{extension}")

        with open(artifact_path, "w", encoding="utf-8") as file:
            file.write(content)

    def save(self):
        """
        Save the structured JSON log for this run.
        """

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
