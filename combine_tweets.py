#!/usr/bin/env python2
# -*- coding: latin-1 -*-

import os
import glob
import pandas as pd
import csv

os.chdir("/home/dama/Code/cogs402/Tweets/Clean/")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# add header and remove empty csvs
for csvfile in all_filenames:
    f = open(csvfile, 'w')
    writer = csv.DictWriter(f, fieldnames=["tweet_id", "datetime", "tweet", "handle"])
    writer.writeheader()
    print(csvfile)

    # with open(f, 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        print(csvfile)
        all_filenames.remove(csvfile)

# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# export to csv
combined_csv.to_csv( "combined_tweets.csv", index=False, encoding='utf-8-sig')