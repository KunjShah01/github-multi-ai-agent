from core.adk_agent import ADKAgent
from core.a2a_protocol import A2AMessage

class WriterAgent(ADKAgent):
    def __init__(self):
        super().__init__()

    def build_prompt(self, repo_summary: str) -> str:
        return f"""
You are an expert README generator AI.

Based on the following GitHub repository structure and language analysis, generate a clean, professional, and developer-friendly `README.md` file with the following sections:

1. 📦 Project Title
2. 📝 Project Description
3. 🚀 Installation Instructions
4. 📚 Usage Examples
5. 📁 Folder Structure
6. 🧪 Tests (if any)
7. 💡 Features
8. 👨‍💻 Contributing
9. 📄 License
10. 🙏 Acknowledgements (if applicable)

Avoid guessing if information is missing. Be accurate, readable, and structured.

Here is the repo summary:
{repo_summary}

scss
Copy
Edit
"""

    def run(self, incoming_message: A2AMessage):
        if incoming_message.message_type != "repo_summary":
            return A2AMessage(
                from_agent="WriterAgent",
                to_agent="UI",
                message_type="error",
                content="WriterAgent only handles 'repo_summary' messages."
            )

        prompt = self.build_prompt(incoming_message.content)
        readme_text = self.generate(prompt)

        return A2AMessage(
            from_agent="WriterAgent",
            to_agent="VisionAgent",
            message_type="readme_draft",
            content=readme_text
        )