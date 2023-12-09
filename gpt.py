import requests
from openai import OpenAI
import math
import os
from dotenv import load_dotenv
from fixblocking import NoBlock


class AI:

    def __init__(self, prompt):
        self.prompt = prompt

    def askAI(self):
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
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

    def stockName(self):
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            # api_key="",
        )
        print("Waiting for response...")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",

            messages=[
                # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user",
                 "content": "Please, give me ONLY a stock name in a 4 letter format for example 'AAPL' that is related to discription " + self.prompt},
            ]
        )
        return completion.choices[0].message.content


    def coef(self, info, stock):
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            # api_key="",
        )
        print("Waiting for response...")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",

            messages=[
                # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user",
                 "content": f"Please, return a number in the range from -1 to 1 where 1 means that news about the the stock {stock} "
                            f"are good, -1 mean that news about the {stock} are bad and 0 means that news about the stock {stock} is neutral or there isn't sufficient information about it. "
                            f"For example if provided summary is negative news about company then your output would like this:-1."
                            f"MOST IMPORTANTLY, NEVER DISPLAY ANYTHING ELSE EXCEPT ONE NUMBER!"
                            f"Here is the summary of article that relates to the stock " + info},
            ]
        )
        return completion.choices[0].message.content

    # def process_answer(self, string):
    #     leng=len(string)
    #     if len(string)>2000:
    #
