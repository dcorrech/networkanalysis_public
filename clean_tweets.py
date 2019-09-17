#!/usr/bin/env python2
# -*- coding: latin-1 -*-
import csv
import json
from datetime import datetime
import os
import re
import numpy as npy

def word_in_text(word, text): 
    # from https://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, text)
    return bool(matches)

date_from = datetime.strptime('2018-03-01 00:00:00', '%Y-%m-%d %H:%M:%S')
date_to = datetime.strptime('2019-03-01 00:00:00', '%Y-%m-%d %H:%M:%S')

count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0
count12 = 0
count13 = 0
count14 = 0
count15 = 0
count16 = 0
count17 = 0
tweets = []

for filename in os.listdir('/home/dama/Code/cogs402/Tweets'):
    print('cleaning ' + filename)
    if filename != 'Clean':
        with open('/home/dama/Code/cogs402/Tweets/' + filename, 'rb') as inp, open('/home/dama/Code/cogs402/Tweets/Clean/' + filename[:-4] + '_edit.csv', 'wb') as out:
            writer = csv.writer(out)
            acc = 0
            for row in csv.reader(inp):
                if acc > 0: 
                    date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                    text = row[2]
                    if  date_to > date > date_from:
                        if word_in_text('Kinder Morgan', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count1 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('pipeline', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count2 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('pipelines', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count3 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('transmountain', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count4 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('KM', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count5 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('NEB', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count6 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('National Energy Board', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count7 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('killer whales', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count8 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('TMX', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count9 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('tankers', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count10 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('oil', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count11 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('oléoduc', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count13 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('orques', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count15 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('orcas', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count16 += 1
                            tweets.append(row)
                            print(len(tweets))
                        elif word_in_text('pétroliers', text):
                            row.append(filename[:-11])
                            writer.writerow(row)
                            count17 += 1
                            tweets.append(row)
                            print(len(tweets))
                else:
                    writer.writerow(["tweet_id", "datetime", "tweet", "handle"])
                    acc += 1
print('Kinder Morgan: ' + str(count1))
print('pipeline: ' + str(count2))
print('pipelines: ' + str(count3))
print('transmountain: ' + str(count4))
print('KM: ' + str(count5))
print('NEB: ' + str(count6))
print('National Energy Board: ' + str(count7))
print('killer whales: ' + str(count8))
print('TMX: ' + str(count9))
print('tankers: ' + str(count10))
print('oil: ' + str(count11))
print('oleoduc: ' + str(count13))
print('orques: ' + str(count15))
print('orcas: ' + str(count16))
print('petroliers: ' + str(count17))

npy.save('/home/dama/Code/cogs402/poli_at.npy', tweets)
