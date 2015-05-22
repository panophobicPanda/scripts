#!/usr/bin/env python
#https://github.com/akabdog 2015-04-06

import json
import glob
import os
#from pprint import pprint

newest = max(glob.iglob('/var/lib/aws/opsworks/chef/*.json'), key=os.path.getctime)

with open(newest) as data_file:
        data = json.load(data_file)
print data[u'opsworks'][u'stack'][u'name']

#use the following line to print all json values
#pprint(data)
