import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import psycopg2
#from sci-kit learn import sklearn 
from sklearn.preprocessing import MinMaxScaler


url="https://finance.yahoo.com/markets/stocks/most-active/"

def get_stock_code(soup_eg):
    code=[]
    for stock_code in soup_eg:
        c=stock_code.find('span')
        if c:
            c=c.text.strip()
            code.append(c)
    return code

def get_stock_name(soup_eg):
    code=[]
    for stock_name in soup_eg:
        name=stock_name.find('span',class_="yf-138ga19 longName")
        if name:
            name=name.text.strip()
            code.append(name)
    return code


def get_market_price(soup_eg):
    pr=[]
    for market_price in soup_eg:
        if market_price.get('data-field')=='regularMarketPrice':
            price=market_price.get('data-value')
            if price:
                pr.append(price)
    return pr


def get_market_change(soup_eg):
    pr=[]
    for market_price in soup_eg:
        if market_price.get('data-field')=='regularMarketChange' and market_price.get('data-tstyle')=='default':
            price=market_price.get('data-value')
            if price:
                pr.append(price)
    return pr


def get_market_change_percent(soup_eg):
    pr=[]
    for market_price in soup_eg:
        if market_price.get('data-field')=='regularMarketChangePercent' and market_price.get('data-tstyle')=='default':
            price=market_price.get('data-value')
            if price:
                pr.append(price)
    return pr


def get_market_volume(soup_eg):
    pr=[]
    for market_price in soup_eg:
        if market_price.get('data-field')=='regularMarketVolume':
            price=market_price.get('data-value')
            if price:
                pr.append(price)
    return pr


def get_market_cap(soup_eg):
    pr=[]
    for market_price in soup_eg:
        if market_price.get('data-field')=='marketCap':
            price=market_price.get('data-value')
            if price:
                pr.append(price)
    return pr


def extract(**kwargs):
    url=kwargs['url']
    response= requests.get(url)
    if not response:
        return "Failed to Retrieve Page"
    soup= BeautifulSoup(response.content, 'html.parser')
    soup_1=soup.find_all('a',class_="ticker medium hover stacked yf-138ga19")
    soup_2= soup.find_all('fin-streamer', limit=175)
    
    #dataframe= pd.DataFrame()
    
    stock_code=get_stock_code(soup_1)
    stock_name=get_stock_name(soup_1)
    
    market_price=get_market_price(soup_2)
    market_change=get_market_change(soup_2)
    market_change_percent=get_market_change_percent(soup_2)
    market_volume= get_market_volume(soup_2)
    market_cap=get_market_cap(soup_2)

    stocks=[]
    for i in range(len(stock_code)):
        stocks.append({
            'Stock Code' : stock_code[i],
            'Stock Name' : stock_name[i],
            'Market Price' : market_price[i],
            'Market Change' : market_change[i],
            'Market Change %' : market_change_percent[i],
            'Volume' : market_volume[i],
            'Market Cap' : market_cap[i]
    
        })



    '''data = {
        'Stock Code': stock_code,
        'Stock Name': stock_name,
        'Market Price': market_price,
        'Market Change': market_change,
        'Market Change %': market_change_percent,
        'Volume': market_volume,
        'Market Cap': market_cap
    }'''

    json_rows= json.dumps(stocks)

    kwargs['ti'].xcom_push(key='stock_rows', value= json_rows)

    return "OK"



def transform(**kwargs):
    data=kwargs['ti'].xcom_pull(key='stock_rows', task_ids='extract_data_from_yahoo_finance_stock_data')

    data=json.loads(data)

    df=pd.DataFrame(data)

    scaler=MinMaxScaler()
    df1=df.iloc[:,2:7]
    df2=df.iloc[:,0:2]

    d=scaler.fit_transform(df1)

    scaled_df=pd.DataFrame(d, columns=df1.columns)

    final_df=pd.concat([df2,scaled_df], axis="columns")

    kwargs['ti'].xcom_push(key='stock_rows', value=final_df.to_json())

    return "OK"


def load(**kwargs):

    data=kwargs['ti'].xcom_pull(key='stock_rows',task_ids='Transform_Stock_Data')


    data=json.loads(data)

    df=pd.DataFrame(data)

    conn = psycopg2.connect(
        host="postgres",  # PostgreSQL service name from Docker Compose
        database="airflow",  # The name of the database
        user="airflow",  # The username
        password="airflow"  # The password
    )
    
    # Insert DataFrame rows into PostgreSQL
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO stocks (stock_code, stock_name, market_price, market_change, market_change_percent, volume, market_cap) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (row['Stock Code'], row['Stock Name'], row['Market Price'], row['Market Change'], 
              row['Market Change %'], row['Volume'], row['Market Cap']))
    
    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

