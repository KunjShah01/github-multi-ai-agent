from core.adk_agent import ADKAgent
from core.a2a_protocol import A2AMessage


class FeedbackAgent(ADKAgent):
    def __init__(self):
        super().__init__()

    def build_feedback_prompt(self, original_readme: str, user_feedback: str) -> str:
        return f"""
You're an AI README editor.

Here is the original README:
{original_readme}

kotlin
Copy
Edit

The user has provided this feedback or edited version:
{user_feedback}

scss
Copy
Edit

Update the README accordingly to improve clarity, correctness, and usefulness. Keep formatting clean and do not hallucinate missing content.
"""

    def run(self, feedback_text: str, previous_msg: A2AMessage):
        if previous_msg.message_type not in ["readme_draft", "readme_with_vision"]:
            return A2AMessage(
                from_agent="FeedbackAgent",
                to_agent="UI",
                message_type="error",
                content="Expected a previous README message."
            )

        prompt = self.build_feedback_prompt(previous_msg.content, feedback_text)
        updated_readme = self.generate(prompt)

        return A2AMessage(
            from_agent="FeedbackAgent",
            to_agent="ExportAgent",
            message_type="final_readme",
            content=updated_readme
        )