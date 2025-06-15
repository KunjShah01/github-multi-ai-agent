import os
import tempfile
from git import Repo
from core.a2a_protocol import A2AMessage


class AnalyzerAgent:
    def __init__(self):
        pass

    def clone_repo(self, github_url):
        try:
            tmp_dir = tempfile.mkdtemp()
            Repo.clone_from(github_url, tmp_dir)
            return tmp_dir
        except Exception as e:
            raise Exception(f"Failed to clone repo: {e}")

    def extract_structure(self, path):
        structure = []
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = '  ' * level
            structure.append(f"{indent}- {os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for f in files:
                structure.append(f"{subindent}- {f}")
        return "\n".join(structure)

    def detect_languages(self, path):
        ext_count = {}
        for root, _, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[-1]
                ext_count[ext] = ext_count.get(ext, 0) + 1

        top_exts = sorted(ext_count.items(), key=lambda x: x[1], reverse=True)[:5]
        return ", ".join([f"{ext}: {count}" for ext, count in top_exts if ext])

    def run(self, github_url):
        local_path = self.clone_repo(github_url)
        structure = self.extract_structure(local_path)
        langs = self.detect_languages(local_path)

        summary = f"Repository structure:\n{structure}\n\nDetected languages:\n{langs}"
        message = A2AMessage(
            from_agent="AnalyzerAgent",
            to_agent="WriterAgent",
            message_type="repo_summary",
            content=summary
        )

        return message
