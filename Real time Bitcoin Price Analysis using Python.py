#!/usr/bin/env python
# coding: utf-8

# # <center><u>Real time Bitcoin Price Analysis using Python</u><center>
# <span>This Notebook has the code to retrieve the real-time Stock price data for bitcoin(using the Coinbase API).The resistance and support levels are defined as follows:<br> <b> Resistance level= Avg one week price+ 10%(estimated VaR Level); <br>
#     Support level = Avg one week's price - 10% </b><br>
#     This is supported by a <b><u>Real Time bitcoin Notification Alert  System</u></b> providing a message on <u><b>my telegram</b></u> when the Resistance and Support levels are touched. It was created using the Telegram bot services to get the required Token and User_Id for setting a connection between the sender and the reciever.

# In[1]:


#Installing the basic library
get_ipython().system('pip install coinbase')


# In[2]:


# Get the BTC Stock price data using the clients
from coinbase.wallet.client import Client
coinbase_API_Key= "################"
coinbase_API_Secret= "################################"
client = Client(coinbase_API_Key, coinbase_API_Secret)


# In[3]:


currency_code = 'BTC-USD'  
# Start the request
price = client.get_spot_price(currency=currency_code)

print ('Current bitcoin price in %s: %s' % (currency_code, price.amount))


# ### Calculate the Support and the Resistance levels

# In[4]:


get_ipython().system('pip install yfinance')


# In[5]:


import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import datetime
from scipy.stats import norm


# In[6]:


data = yf.download(tickers='BTC-USD', period='14d', interval='1d')
data


# In[7]:


#Mean for one week price data
data['MAS']= data['Close'].rolling(7).mean()
data['Resistance Alert']= data['MAS']+0.1*data['MAS']
data['Support Alert']=data['MAS']-0.1*data['MAS']
data


#  ## Candlestick plot for BTC Price Analysis

# In[8]:


#Bitcoin one minute interval data
data1=yf.download(tickers='BTC-USD', period='1d', interval='1m')
data1


# In[9]:


#Plot with Candlesticks using plotly library
fig1=go.Figure()
#candlestick
fig1.add_trace(go.Candlestick(x=data1.index,open=data1['Open'],high=data1['High'], low=data1['Low'], close=data1['Close'], name='market data'))
#Add titles
fig1.update_layout(title='BTC live share price evolution', yaxis_title='Stock Price (USD per Shares)')
#X-Axis
fig1.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
       buttons=list((
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
           dict(step="all")
        ))
    )
)
fig1.show()


# ## Sending Alerts using Telegram

# In[13]:


get_ipython().system('pip install requests')
import requests
import time

# global variables
bot_token = '##############################################'
chat_id = '**********'


# In[11]:


# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)


# In[ ]:


#The main function for setting the calculated level alerts and sending an sms on telegram once the levels equal the current stock price data
def main():
    last_price=-1
    while True:
        currency_code = 'BTC-USD'  
        # Start the request
        price = client.get_spot_price(currency=currency_code)
        if price.amount!= last_price:
            print('Bitcoin price:',price.amount)
            last_price=price.amount
            if float(last_price)>data['Resistance Alert'][len(data)-1]:
                send_message(chat_id=chat_id, msg=f'BTC Resistance Alert is activated. The current Price is: {last_price}')
            elif float(last_price)<data['Support Alert'][len(data)-1]:
                send_message(chat_id=chat_id, msg=f'BTC Support Alert is activated. The current Stock Price is: {last_price}')    
main()


# ### <center>This marks the end of this Notebook</center>
# Following are the references used:<br>
# 1.Coinbase Documentation-https://developers.coinbase.com/api/v2<br>
# 2.https://thecodingpie.com/post/lets-build-a-real-time-bitcoin-price-notification-python-project<br>
# 3.Plotly Documentation-https://plotly.com/python/

# In[ ]:




