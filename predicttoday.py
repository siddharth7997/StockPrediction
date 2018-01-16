#hello
#if you get any problem while running it please mail me @ siddharth7997@gmail.com
#Siddharth Panigrahi signing out.


print "Stock Prediction using Lstm <Historical Data and Semantic Analysis on News>"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import datetime
import math, time
import itertools
from sklearn import preprocessing
import datetime
from operator import itemgetter
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
import datetime
import warnings

def get_stock_data(stock_name,market_name,normalized=0):
    #getting todays date
    today=datetime.datetime.now()
    #dictionary for the months for Google Finance API
    month={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    #https://finance.google.com/finance/historical?q=NASDAQ:AAPL&num=30&ei=-8_DWfi2NMOYuQSr3424BA&startdate=Sep+21%2C+2014&enddate=Sep+21%2C+2017&output=csv
    url="https://finance.google.com/finance/historical?q="+market_name+":"+stock_name+"&num=30&ei=-8_DWfi2NMOYuQSr3424BA"+"&startdate="+month[today.month]+"+"+str(today.day)+"%2C+"+str(today.year-2)+"&enddate="+month[today.month]+"+"+str(today.day)+"%2C+"+str(today.year)+"&output=csv"
    
    col_names = ['Date','Open','High','Low','Close','Volume']
    stocks = pd.read_csv(url,header=0, names=col_names)
    
    df_stocks= pd.DataFrame(stocks)
    
    sem_cols=['Date','Semantic']
    semantic=pd.read_csv('semantic/semantic.csv',header=0,names=sem_cols)
    df_semantics=pd.DataFrame(semantic)
    df=pd.merge(semantic,stocks,how='inner',left_on=None, right_on=None)
    df=df[::-1]
    df_date=df.copy()
    df.drop(df.columns[[0,4,6]], axis=1, inplace=True)
    df_date.drop(df_date.columns[[4,6]], axis=1, inplace=True)
    columns=['Open','High','Close']
    df[columns] = df[columns].convert_objects(convert_numeric=True)
    df[columns] = df[columns].astype('float64')
    
    
    avghigh=sum(df['High'][:7])/7
    avgclose=sum(df['Close'][:7])/7
    avgopen=sum(df['Open'][:7])/7
    avgsemantic=sum(df['Semantic'][:7])/7
    #print avghigh,avgclose,avgopen,avgsemantic
    
    df2 = pd.DataFrame([[avgsemantic,avgopen,avghigh,avgclose]], columns=['Semantic','Open','High','Close'])
    df2=df2.append(df, ignore_index=True)
    #print "in function",df2

    
    #print df.dtypes
    return df2,df_date

def model_data(stock,seq_len):
    features=len(stock.columns)
    data=stock.as_matrix()
    #print data

#main lstm !--! Yo ready for work
def build_model2(layers):
    d = 0.2
    model = Sequential()
    model.add(LSTM(128, input_shape=(layers[1], layers[0]), return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(64, input_shape=(layers[1], layers[0]), return_sequences=False))
    model.add(Dropout(d))
    model.add(Dense(16,init='uniform',activation='relu'))        
    model.add(Dense(1,init='uniform',activation='relu'))
    model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
    return model

def load_data(stock, seq_len):
    amount_of_features = len(stock.columns)
    data = stock.as_matrix() #pd.DataFrame(stock)
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    result = np.array(result)
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    x_train = train[:, :-1]
    y_train = train[:, -1][:,-1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:,-1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))  

    return [x_train, y_train, x_test, y_test]


warnings.filterwarnings('ignore')
stock_name = raw_input('Please enter company code ex:GOOGL,MSFT,AAPL,INFY:')
market_name= raw_input('Please enter market code ex:NASDAQ,NASDAQ,NASDAQ,NYSE:')
df,df_date= get_stock_data(stock_name,market_name,0)
#print "df---------------------------"
#print df.tail()
#print "df with date-----------------"
#print df_date.tail()

maxhigh=max(df['High'])
maxclose=max(df['Close'])
maxopen=max(df['Open'])
df['High']=df['High']/max(df['High'])
df['Close']=df['Close']/max(df['Close'])
df['Open']=df['Open']/max(df['Open'])

avghigh=sum(df['High'][:7])/7
avgclose=sum(df['Close'][:7])/7
avgopen=sum(df['Open'][:7])/7
avgsemantic=sum(df['Semantic'])/7

#print df.head()

window = 5
X_train, y_train, X_test, y_test = load_data(df[::-1], window)
#print("X_train", X_train.shape)
#print("y_train", y_train.shape)
#print("X_test", X_test.shape)
#print("y_test", y_test.shape)
print "\n\n-------------------------------------------------------------------------------------------------------------------"
model = build_model2([4,window,1])

model.fit(
    X_train,
    y_train,
    batch_size=512,
    nb_epoch=500,
    validation_split=0.1,
    verbose=0)

print "\n\n-------------------------------------------------------------------------------------------------------------------"
print "Ignore Warnings :)"


print "\n\n"
trainScore = model.evaluate(X_train, y_train, verbose=0)
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore[0], math.sqrt(trainScore[0])))

testScore = model.evaluate(X_test, y_test, verbose=0)
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore[0], math.sqrt(testScore[0])))


p = model.predict(X_test)

diff=[]
ratio=[]

for u in range(len(y_test)):
    pr = p[u][0]
    ratio.append((y_test[u]/pr)-1)
    diff.append(abs(y_test[u]- pr))

total=0;
ct=0;
for g in ratio:
    if not math.isnan(g):
        total=total+g
        ct=ct+1
error=total/ct

if not math.isnan(error):
	print "average error rate :",abs(error*100)
	print "\n\n"
	print "stock name",stock_name,"date",datetime.datetime.now()
	print"\n\n"
	print "Prediction for today close price:",p[len(p)-1][0]*maxclose*(1+error)
else:
	print "Looks Like Model Din't Train properly! Rerun it!"
