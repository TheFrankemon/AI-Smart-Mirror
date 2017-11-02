# -*- coding: utf-8 -*-
import pyrebase
import json
import os

usr = ""
pwd = ""
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

	def add(self, name, img_1, img_2):
		try:
			db = firebase.database()
			storage = firebase.storage()

			imgpath = os.path.join(fileDir, img_1)
			filename = name + '/1.png'
			storage.child(filename).put(imgpath)
			imgpath = os.path.join(fileDir, img_2)
			filename = name + '/2.png'
			storage.child(filename).put(imgpath)
			img1url = storage.child(filename).get_url(None)

			data = {"name": name, "img1": img1url, "img2": img1url}
			db.child("clients").push(data)

		except Exception as e:
			print("Failed to parse images")
			print(e)
			traceback.print_exc()
			return
