import requests
from datetime import datetime as dt
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Use https://www.alphavantage.co/documentation/#daily

parameters_for_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "ETRMOZN1CGQ7ALEP"
}

# API_URL = https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=ETRM0ZN1CQ7ALEP

response_from_stocks = requests.get(STOCK_ENDPOINT, params=parameters_for_stock)
response_from_stocks.raise_for_status()
stocks_by_days = response_from_stocks.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stocks_by_days.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

diff_between_stocks = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
stock_up_or_down = None
if diff_between_stocks > 0:
    stock_up_or_down = "📈"
else:
    stock_up_or_down = "📉"

percentage_diff = round((diff_between_stocks / float(yesterday_closing_price)) * 100)

if abs(percentage_diff) > 0:
    parameters_for_news = {
        "apiKey": "Your API Key",
        "q": COMPANY_NAME
    }
    response_from_news = requests.get(url=NEWS_ENDPOINT, params=parameters_for_news)
    response_from_news.raise_for_status()    

    list_of_articles = response_from_news.json()["articles"][:3]


    formatted_articles = [f"{STOCK_NAME}: {stock_up_or_down}{percentage_diff}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in
                          list_of_articles]

    account_sid = "Twilio Account SID"
    auth_token = "Twilio Auth Token"
    twilio_phone_number = "Twilio Phone Number"
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=twilio_phone_number,
            to="Your Phone Number"
        )

