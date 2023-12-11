from openai import OpenAI
import math
import json
import os
import requests
from gpt import AI
import typing
from fixblocking import NoBlock
import asyncio
import yfinance as yf



# get all stock info

class News:

    def __init__(self, prompt):
        self.prompt = prompt
        self.stock=""
        self.ai=AI(prompt=self.prompt)


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

    def getStock(self):
        try:
            stock1=yf.Ticker(self.prompt)
            price=stock1.info["currentPrice"]
            self.stock = self.prompt
            return self.prompt.upper()
        except:
            stock2 = self.ai.stockName()
            try:
                check = yf.Ticker(stock2)
                price = check.info["currentPrice"]
            except:
                return -1
            print(stock2)
            return stock2

    def getStockPrice(self):
        price=0
        try:
            stock1=yf.Ticker(self.prompt)
            price=stock1.info["currentPrice"]
            self.stock = self.prompt
            return [self.stock,price]
        except:
            stock2 = self.ai.stockName()
            try:
                check = yf.Ticker(stock2)
                price = check.info["currentPrice"]
            except:
                return -1
            print(stock2)
            return [stock2,price]


    async def getNews(self):
        stock=self.getStock()
        if not stock == -1:
            api = os.getenv("NEWS_API_KEY")
            # api="demo"
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={api}'
            r = requests.get(url)
            data = r.json()
            print(data)
            task = asyncio.create_task(self.parseJSON(data))
            res = await task
            return res


