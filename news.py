from openai import OpenAI
import math
import json
import os
import requests
from gpt import AI
import typing
from fixblocking import NoBlock
import asyncio

class News:

    def __init__(self, prompt):
        self.prompt = prompt
        self.stock=""
        self.ai=AI(prompt=self.prompt)

    def getStock(self):
        stockName= self.ai.stockName()
        print(stockName)
        return stockName

    @NoBlock.to_thread
    def parseJSON(self, json):
        coefSum=0
        numIterations = 0

        for summary in json["feed"]:
            coeficient = self.ai.coef(str(summary["title"]+". "+summary["summary"]), self.stock)
            print(coeficient)
            coefSum+=float(coeficient)
            numIterations += 1
            if numIterations == 10:
                break

        print("CoefSum:"+str(coefSum))
        print("numIterations:" + str(numIterations))
        totalCoef=coefSum/numIterations


        print("Total coefficient: "+str(totalCoef))
        return str(totalCoef)

    async def getNews(self):
        api = os.getenv("NEWS_API_KEY")
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.prompt}&apikey={api}'
        r = requests.get(url)
        data = r.json()
        print(data)

        if 'Information' in data:

            stock = self.getStock()
            print(stock)
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={api}'
            r = requests.get(url)
            data = r.json()

            if "Information" in data:
                return "Stock name not found"

            task= asyncio.create_task(self.parseJSON(data))
            res = await task
            self.stock=stock
            return res

        else:

            self.stock = self.prompt
            print(self.stock)
            task = asyncio.create_task(self.parseJSON(data))
            res = await task
            return res

