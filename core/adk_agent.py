import google.generativeai as genai
import os

class ADK:
    def __init__(self,model_name="gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        genai.configure(api_key=self.api_key)   
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt:str)->str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f" Error generating : {str(e)}"
