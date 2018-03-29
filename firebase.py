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

	def add(self, name, img_1, img_2, timestamp):
		try:
			db = firebase.database()
			storage = firebase.storage()

			imgpath = os.path.join(fileDir, img_1)
			filename = name + '/1.jpg'
			storage.child(filename).put(imgpath)
			img1url = storage.child(filename).get_url(None)
			imgpath = os.path.join(fileDir, img_2)
			filename = name + '/2.jpg'
			storage.child(filename).put(imgpath)
			img2url = storage.child(filename).get_url(None)

			userdata = {"img1": img1url, "img2": img2url, "isCompleted": False, "name": name, "ts": timestamp, "user": "", "userUID": "", "comment": ""}
			db.child("clients").push(userdata)

			logdata = {"client": name, "event": "ARRIVED", "ts": timestamp}
			db.child("eventlog").push(logdata)

		except Exception as e:
			print("Failed to save images")
			print(e)
			traceback.print_exc()
			return
