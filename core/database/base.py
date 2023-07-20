"""
base function connect Davinci database
"""
from pymongo import MongoClient

client = MongoClient(host='127.0.0.1', port=27017)
davinci_db = client.DaVinchi
surgery = davinci_db.surgery
user = davinci_db.user
apparatus = davinci_db.apparatus
supplies = davinci_db.supplies

