from core.a2a_protocol import A2AMessage
import os


class ExportAgent:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    def save_readme(self, content: str, filename="README.md"):
        path = os.path.join(self.export_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def run(self, message: A2AMessage):
        if message.message_type != "final_readme":
            return A2AMessage(
                from_agent="ExportAgent",
                to_agent="UI",
                message_type="error",
                content="Expected final_readme message."
            )

        saved_path = self.save_readme(message.content)

        return A2AMessage(
            from_agent="ExportAgent",
            to_agent="UI",
            message_type="readme_saved",
            content=f"README saved to: {saved_path}"
        )
