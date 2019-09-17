#!/usr/bin/env python2
# -*- coding: latin-1 -*-
import csv
import json
from datetime import datetime
import os
import re
import numpy as npy

poli_at = npy.load('/home/dama/Code/cogs402/poli_at.npy')

#sort the array
poli_at = poli_at[poli_at[:,1].argsort()] #doesn't seem to work, we'll figure it out

j = 0
for i in range(0, len(poli_at) - 1):
    print(poli_at[i])
    j += 1
print('total tweets = ' + str(j))
print('length of poli_at = ' + str(len(poli_at)))
npy.save('/home/dama/Code/cogs402/poli_at.npy', poli_at)