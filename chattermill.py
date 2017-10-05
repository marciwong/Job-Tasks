#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:59:20 2017

@author: marcowong
"""
import pandas as pd
import numpy as np
import csv
import sqlite3

# Creating SQL cursor
data = sqlite3.connect('/Users/marcowong/Desktop/data-challenge-master/exercise_database.db')
d = data.cursor()

df = pd.read_csv('/Users/marcowong/Desktop/data-challenge-master/reddit_exercise_data.csv')

#Creating 4 buckets for AppBought and MoneySpent (Quantiles)

firstQuantileApp = np.percentile(df.iloc[:,6],25)
secondQuantileApp = np.percentile(df.iloc[:,6],50)
thirdQuantileApp = np.percentile(df.iloc[:,6],75)
fourthQuantileApp = np.percentile(df.iloc[:,6],100)

firstQuantileMoney = np.percentile(df.iloc[:,7],25)
secondQuantileMoney = np.percentile(df.iloc[:,7],50)
thirdQuantileMoney = np.percentile(df.iloc[:,7],75)
fourthQuantileMoney = np.percentile(df.iloc[:,7],100)

app_bought_bucket = []
money_spent_bucket = []

for i in range(0,len(df)):
     #this checks whether any app bought is 0 and money spent is also 0
    if df.iloc[i,6] ==0:
        if df.iloc[i,7] !=0:
            print(i)
    if df.iloc[i,7] ==0:
        if df.iloc[i,6] !=0:
            print(i)           
    # at index 309, app_bought is 0 and money_spent is not 0.
    # at index 243, 246, money_spent is 0 and app_bought is not 0.
    # not very sure what do the variables mean, so it maybe something we may worth take care of
    
    
    #### separating buckets (into quantiles)
    if df.iloc[i,6] <= firstQuantileApp:
        app_bought_bucket.append(1)
    elif firstQuantileApp < df.iloc[i,6] <= secondQuantileApp:
        app_bought_bucket.append(2)
    elif secondQuantileApp < df.iloc[i,6] <=thirdQuantileApp:
        app_bought_bucket.append(3)
    elif thirdQuantileApp < df.iloc[i,6] <= fourthQuantileApp:
        app_bought_bucket.append(4)
                
    if df.iloc[i,7] <= firstQuantileMoney:
        money_spent_bucket.append(1)
    elif firstQuantileMoney < df.iloc[i,7] <= secondQuantileMoney:
        money_spent_bucket.append(2)
    elif secondQuantileMoney < df.iloc[i,7] <=thirdQuantileMoney:
        money_spent_bucket.append(3)
    elif thirdQuantileMoney < df.iloc[i,7] <= fourthQuantileMoney:
        money_spent_bucket.append(4)

#### inserting the buckets into dataframe
df.insert(8,'app_bought_bucket',app_bought_bucket)
df.insert(9,'money_spent_bucket',money_spent_bucket)

variables = df.columns.tolist()

#rearrange columns to fit database
tempList = [1,0,3,4,5,6,7,8,9]

dbVariable = []

for i in tempList:
    dbVariable.append(variables[i])

df = df[dbVariable]
df.to_csv('chattermill.csv')

#check number of unique numbers to match results of SQL queries
noOfIso = len(list(set(df.iloc[:,2])))
noOfDates = len(list(set(df.iloc[:,4])))

#### writing SQL queries
for i in range(0, len(df)):
    record = df.iloc[i]
    
    review = record.iloc[0]
    title = record.iloc[1]
    iso = record.iloc[2]
    score = int(record.iloc[3])
    date = record.iloc[4]
    apps_bought = int(record.iloc[5])
    money_spent = float(record.iloc[6])
    apps_bought_bucket = str(record.iloc[7])
    money_spent_bucket = str(record.iloc[8])
    
    new_record = (review, title, iso, score, date, apps_bought, money_spent, apps_bought_bucket, money_spent_bucket)
    
    d.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?,?,?)', new_record)

#### Queries for the 3 questions

d.execute('SELECT iso,AVG(score) FROM reviews GROUP BY iso ORDER BY iso')
avgIso = d.fetchall()  
d.execute('SELECT apps_bought_bucket, MAX(score)  FROM reviews GROUP BY apps_bought_bucket ORDER BY apps_bought_bucket')
maxAppBoughtBucket = d.fetchall()
d.execute('SELECT date, AVG(score) FROM reviews GROUP BY date ORDER BY date')
avgDate = d.fetchall()

#### save db file
data.commit()

data.close()

#### writing results in csv files
with open('avgIso.csv', 'w')  as csvfile:
    fieldnames = ['ISO','Average Score by iso']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    
    for i in range(0,len(avgIso)):
        writer.writerow({'ISO':avgIso[i][0],'Average Score by iso' : avgIso[i][1]})

with open('maxAppBoughtBucket.csv', 'w')  as csvfile:
    fieldnames = ['Bucket','Max Score by App Bought Bucket']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    
    for i in range(0,len(maxAppBoughtBucket)):
        writer.writerow({'Bucket':maxAppBoughtBucket[i][0],'Max Score by App Bought Bucket' : maxAppBoughtBucket[i][1]})
        
with open('avgDate.csv', 'w')  as csvfile:
    fieldnames = ['Dates','Average Score by Days']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    
    for i in range(0,len(avgDate)):
        writer.writerow({'Dates': avgDate[i][0],'Average Score by Days' : avgDate[i][0]})
     