"""
base function connect Davinci database
"""
from pymongo import MongoClient

client = MongoClient(host='47.242.250.68', port=27017)
davinci_db = client.DaVinchi
surgery = davinci_db.surgery
user = davinci_db.user
apparatus = davinci_db.apparatus
supplies = davinci_db.supplies
message = davinci_db.message
