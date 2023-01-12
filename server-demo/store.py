#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:17:31 2023

@author: tim
"""
from array import *
import json

store={}
store["a"]=[[1,2],[3,4]]
store["b"]=[[2,3],[5,7]]
print(store)

# represents an transition update
a = store['a']
a[0][1]+=1
store['a']=a

print(store)

# Serializing json
json_object = json.dumps(store)
 
# Writing to store.json
# this could run on a timer, every say 5min or 10min
with open("store.json", "w") as outfile:
    outfile.write(json_object)
    
    
# simulate opening adjancency matrix and load into memory at startup

store={} #remove old store
print("delete store")
print(store)
# Opening JSON file
f = open('store.json')
  
# returns JSON object as 
# a dictionary
store = json.load(f)
f.close()

print("load store")
print(store)


#https://stackoverflow.com/questions/3310049/proper-use-of-mutexes-in-python
#https://websocket-client.readthedocs.io/en/latest/examples.html#dispatching-multiple-websocketapps




