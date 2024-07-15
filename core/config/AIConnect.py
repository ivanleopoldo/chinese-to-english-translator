from dotenv import load_dotenv; load_dotenv()
import os
import openai as api

class AIConnect:
    def __init__(self):
        self.api = api
        self.api.api_key = os.getenv("OPENAI_API_KEY")
        self.api.base_url = os.getenv("API_URL")
        self.api.default_headers = {"x-foo": "true"}

        self.model = "gpt-3.5-turbo"
        self.completions = self.api.chat.completions

    def get_completion(self, to_translate):
        message = self.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a Chinese to English translator. After translating the text, you have to correct the grammatical errors of the translated text."},
                {"role": "user", "content": to_translate}
            ],
        )
        return message

    def translate(self, to_translate):
        return self.get_completion(to_translate).choices[0].message.content
