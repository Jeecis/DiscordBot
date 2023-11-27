from openai import OpenAI
import math
import os
from dotenv import load_dotenv

class AI:

    def __init__(self, prompt):
        self.prompt = prompt

    def askAI(self):
        load_dotenv()
        client = OpenAI(
            api_key=os.getenv("OPENAI_KEY"),
            # api_key="",
        )
        print("Waiting for response...")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",

            messages=[
                # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "NEVER EXCEED 2000 CHARACTERS IN YOUR REPLY"},
                {"role": "user", "content": self.prompt}
            ]
        )
        return completion.choices[0].message.content

    # def process_answer(self, string):
    #     leng=len(string)
    #     if len(string)>2000:
    #
