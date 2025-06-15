import os
from core.adk_agent import ADK
from core.a2a_protocol import A2AMessage
import google.generativeai as genai
from PIL import Image


class VisionAgent(ADK):
    def __init__(self, model_name="gemini-2.5-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def analyze_image(self, image_path, context_prompt="Describe the following system diagram:"):
        try:
            image = Image.open(image_path)
            response = self.model.generate_content([context_prompt, image])
            return response.text.strip()
        except Exception as e:
            return f"❌ Error analyzing image: {e}"

    def run(self, image_path, previous_readme_msg: A2AMessage):
        vision_section = self.analyze_image(image_path)

        enhanced_readme = previous_readme_msg.content + f"\n\n---\n\n🧭 **System Overview**\n{vision_section}"

        return A2AMessage(
            from_agent="VisionAgent",
            to_agent="FeedbackAgent",
            message_type="readme_with_vision",
            content=enhanced_readme
        )
