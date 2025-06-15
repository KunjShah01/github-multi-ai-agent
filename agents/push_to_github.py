import base64
import requests
from core.a2a_protocol import A2AMessage

class GitHubPushAgent:
    def __init__(self, github_token):
        self.token = github_token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_repo_file_sha(self, owner, repo, path):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("sha")
        return None  # File does not exist yet

    def push_readme(self, github_url, readme_text, commit_message="🤖 Auto-generated README"):
        try:
            parts = github_url.replace("https://github.com/", "").split("/")
            owner, repo = parts[0], parts[1]

            path = "README.md"
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            sha = self.get_repo_file_sha(owner, repo, path)

            data = {
                "message": commit_message,
                "content": base64.b64encode(readme_text.encode("utf-8")).decode("utf-8"),
                "branch": "main"  # or "master"
            }
            if sha:
                data["sha"] = sha

            response = requests.put(url, headers=self.headers, json=data)

            if response.status_code in [200, 201]:
                return f"✅ README pushed to GitHub: {github_url}"
            else:
                return f"❌ GitHub push failed: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Exception during GitHub push: {e}"

    def run(self, github_url, message: A2AMessage):
        if message.message_type != "final_readme":
            return A2AMessage(
                from_agent="GitHubPushAgent",
                to_agent="UI",
                message_type="error",
                content="Expected final_readme message."
            )

        result = self.push_readme(github_url, message.content)
        return A2AMessage(
            from_agent="GitHubPushAgent",
            to_agent="UI",
            message_type="github_push_status",
            content=result
        )
