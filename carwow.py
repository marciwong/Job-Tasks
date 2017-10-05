#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:06:10 2017

@author: marcowong
"""
import pandas as pd
import numpy as np
import csv

data = pd.read_csv('/Users/marcowong/Desktop/campaign_data_set.csv')

PCPlist = []
BMM = []
Exact = []
Purchases = []
Core = []
year2016 = []
HeadTerms = []

for i in range(0,len(data)):
    if data['campaign'].iloc[i] == 'xNew-Make:Nissan|Model:Qashqai|Match:BMM':
        BMM.append(data.iloc[i,:])
    if data['campaign'].iloc[i] == 'xNew-Make:Nissan|Model:Qashqai|Match:Exact':
        Exact.append(data.iloc[i,:])
    if data['ad_group'].iloc[i] == 'Make:Nissan|Model:Qashqai|Type:PCP':
        PCPlist.append(data.iloc[i,:])
    if data['ad_group'].iloc[i] == 'Make:Nissan|Model:Qashqai|Type:Core':
        Core.append(data.iloc[i,:])
    if data['ad_group'].iloc[i] == 'Make:Nissan|Model:Qashqai|Type:2016':
        year2016.append(data.iloc[i,:])
    if data['ad_group'].iloc[i] == 'Make:Nissan|Model:Qashqai|Type:Head_Terms':
        HeadTerms.append(data.iloc[i,:])
    if data['purchases'].iloc[i] != 0:
        Purchases.append(data.iloc[i,:])

noOfPurchases = np.sum(data['purchases'])
totalCost = np.sum(data['cost'])

adGroup = pd.unique(data['ad_group'])
ad_group = []
for i in range(0,len(adGroup)):
    ad_group.append(adGroup[i])
    
#purchases = data['purchases']*300
profit = data['purchases']*300 - data['cost']
revenue = [data['ad_group'],data['purchases'],data['cost'],profit,data['signups']]
commission = pd.concat(revenue, axis = 1)
 

#with open('Revenue.csv', 'w')  as f:
#    fieldnames = ['ad_group','commission','cost','profit','signups']
#    writer = csv.DictWriter(f, fieldnames = fieldnames)
#    writer.writeheader()
#    
#    for i in range(0,len(commission)):
#        writer.writerow({'ad_group' : commission.iloc[i,0], 'commission' : commission.iloc[i,1], 'cost':commission.iloc[i,2], 'profit':commission.iloc[i,3], 'signups':commission.iloc[i,4] })
#
#with open('Core.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(Core)
#
#with open('Purchases.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(Purchases)
#
#with open('PCP.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(PCPlist)
#    
#with open('2016.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(year2016)
#    
#with open('HeadTerms.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(HeadTerms)
#
#with open('BMM.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(BMM)
#    
#with open('Exact.csv', 'w')  as f:
#    writer = csv.writer(f)
#    writer.writerow(data.columns)
#    writer.writerows(Exact)

