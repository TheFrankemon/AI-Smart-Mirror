# -*- coding: utf-8 -*-
import pymongo
import json
from bson.binary import Binary

usr = ""
pwd = ""
serverip = ""
dbname = ""
db = None

class Mongo(object):
	def __init__(self):
		with open('config.json') as data_file:
			conf = json.load(data_file)
		global usr, pwd, serverip, dbname
		usr = str(conf["conn"]["usr"])
		pwd = str(conf["conn"]["pwd"])
		serverip = str(conf["conn"]["serverip"])
		dbname = str(conf["conn"]["dbname"])
		self.connect()

	def connect(self):
		try:
			concat = "mongodb://" + usr + ":" + pwd + "@" + serverip + "/" + dbname        
			print("Connecting to DB:..." + concat)
			client = pymongo.MongoClient(concat)
			global db
			db = client.mean
			print("There are " + str(db.clients.count()) + " on the DB")

		except Exception as e:
			print "Failed connection to DB!"
			print(e)
			traceback.print_exc()
			return

	def add(self, name, img_url1, img_url2):
		#binaryimg = Binary(open("/home/pi/AI-Smart-Mirror-Franco/img/c1.png",'rb').read())
		try:
			binaryimg1 = Binary(open(img_url1,'rb').read())
			binaryimg2 = Binary(open(img_url2,'rb').read())
			global db
			db.clients.insert_one({
				"name":name,
				"img1":binaryimg1,
				"img2":binaryimg2
			})

		except Exception as e:
			print "Failed to parse images"
			print(e)
			traceback.print_exc()
			return
