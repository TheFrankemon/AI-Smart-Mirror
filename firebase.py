# -*- coding: utf-8 -*-
import pyrebase
import json
import os

fireconfig = ""
firebase = None
fileDir = os.path.dirname(os.path.realpath('__file__'))

class Firebase(object):
	def __init__(self):
		with open('config.json') as data_file:
			conf = json.load(data_file)
		global usr, pwd, fireconfig
		usr = str(conf["conn"]["usr"])
		pwd = str(conf["conn"]["pwd"])
		fireconfig = conf["conn"]["fireconfig"]
		self.connect()

	def connect(self):
		try:
			global firebase
			firebase = pyrebase.initialize_app(fireconfig)
			print("Connecting to DB:..." + fireconfig["databaseURL"])
		except Exception as e:
			print("Failed connection to DB!")
			print(e)
			traceback.print_exc()
			return

	def add(self):
		try:
			db = firebase.database()
			storage = firebase.storage()

		except Exception as e:
			print(e)
			traceback.print_exc()
			return
