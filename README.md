# DISCORD BOT MONEYMAN
#### Video Demo:  https://youtu.be/9O7bvo3hSwU
#### Description:

My project is a discord bot that is a stock investment helper that provides info in which stock you should invest.

User starts by adding a stock/s o track with command /addstock and then the stock is added to the stock tracking list. 
You can also write a stock description in the provided prompt space and the bot will still understand what type of stock it is.

The main functionality is that for each stock reads 10 news per 1 iteration about and rates each of the news article  if they are negative, neutral or positive and returns for each of the news it returns a number -1, 0 or 1 respectively.  
Then the investment case coefficient is calculated by summing up the previously mentioned news positiveness numbers and dividing them by the total news the bot read which usually is 10 if nothing goes wrong. 
From investment case coefficient you can decipher whether to invest in this stock or not.
Additionally, if you need a little help regarding investing or anything else you can just ask the in-built AI bot to help using command /ai

Since at the start of the project I was considering to use web scraping instead of using news API I also created a /news functionality, where my bot can retrieve the latest news from a news website, however, this only work with some websites such as delfi.lv, lsm.lv or aljazeera.com.
And similarly to stocks you can also track news by running command /addnews and then /startnewsloop where the bot will send you the latest news of specified website hourly. 

In total this project took me around 25 hours

### Projects infastructure

bot.py file contains all of the bot commands and their functionalities additionally it is the file that you run to start your discord bot since it contains the discords api bot.run() function.
Since one of the problems I encountered was that discord API timed out when waiting for a specific task to finish, I had to make some of the functions non-blocking or in other words there are functions that block the whole thread, thus hindering the execution.
To make them non-blocking I used typing, and async libraries to specify he return values and async to mek the function non-blocking.
And to use this functionality in bot.py commands I made a separate class so I would just need to reference it in decorators.

fixblocking.py as mentioned previously makes functions non-blocking so they don't stop the whole program.

WebScraping.py uses BeautifulSoup library to scrape the news from the websites. I tried to generalise the webscraping for most of the websites, however, it didn't work.
I specifically tried retrieving the link to the article which usually is placed in <article> tag of websites html, but it turns out that that is not really true and other websites use other html structures.
This is still an unsolved challenge, but it doesn't really affect the main functionality of the code.

gpt.py contains all the methods that uses OpenAI gpt-3.5 functionality. These methods are used by other functions in news.py or bot.py files.
Mainly in this class the hardest part was to write the correct prompt for coef and stockName functions, however with trial and error I managed to get a fairly efficient prompt that has a good success rate.

news.py is a file contains all the functions regarding stock news. 
It uses aplphavantage api to get news summaries about specific stocks and yahoo finance api to get specific information about the stock.
Yahoo finance api allows me to retrieve the information about a stock much faster than alphavantage so in some cases it made sense to use it.
Additionally, it provides also the current stock price in methods like getprice()
The most challenging part here was parseJSON() method which in short calculates the coefficient with the news. 
In some cases, ths function just decided not to work and it was a bit of a challenge to connect gpt.py methods with alphavantage api.

Most importantly, a very challenging part was learning more about pythons OOP, concurrency and decorator concepts without which this whole project wouldn't be possible.

### Bot commands

AI:

/ai - chat with chatGPT


Stocks:

/addstock - adds stock to track

/getprice - get price of any stock

/startstockloop - the bot will start looping through stock news and provide coefficient in the interval from -1 to 1 on whether you should invest in the stock that's being tracked

/stopstockloop - the bot will stop the stock loop


News (works only on few specific websites such as delfi.lv or lsm.lv):

/addnews - sets news website to track

/news - get the latest news

/startnewsloop - the bot will start looping through news and print the latest news every hour

/stopnewsloop - the bot will stop looping through news 


Hidden commands (not meant to be executed by every user):

/sync - syncs all the bot.tree commands

/setCID - sets the channel ID where the bot should send messages


### How to test it
Since hosting a discord bot with gpt integration isn't cheap the steps will be more complicated.

Download this projects file and open it in your favourite IDE (Pycharm or Vscode)

You will have to set your own API keys in environmental variables, but I will just provide the API key names mentioned in my program and to which API they are related:

For OpenAI API - OPENAI_API_KEY

For Alphavantage news API - NEWS_API_KEY

For Discord bot API - DISCORD_API_KEY (for this you will have to create your own discord bot)


After setting the API keys you should be set and just run the program ;)