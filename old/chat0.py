from dotenv import load_dotenv
import openai
load_dotenv()  # This loads variables from .env into os.environ
client = openai.OpenAI()  

from typing import Optional
# Chat class using new openai.ChatCompletion
class Chat:
    def __init__(self, system: Optional[str] = None):
        self.system = system
        self.messages = []

        if system is not None:
            self.messages.append({
                "role": "system",
                "content": system
            })

    def prompt(self, content: str) -> str:
        self.messages.append({
            "role": "user",
            "content": content
        })

        # NEW: use openai.ChatCompletion with `.with_messages().create()`
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        response_content = response.choices[0].message.content
        self.messages.append({
            "role": "assistant",
            "content": response_content
        })
        return response_content