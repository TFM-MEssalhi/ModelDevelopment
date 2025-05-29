import os
import openai
from dotenv import load_dotenv
load_dotenv()

class LLMmodel:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=os.getenv("OPENAI_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = os.getenv("OPEN_ROUTER_MODEL", "google/gemini-2.0-flash-001")
        
    def ask_model(self, prompt):
        try:
            respuesta = self.client.chat.completions.create(
                    extra_headers={},
                    extra_body={},
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                            ]
                        }
                    ]
                )
            return respuesta.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error: {e}")
            return None