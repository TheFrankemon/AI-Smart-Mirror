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
		global fireconfig
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
			return

	def add(self, name, img_1, img_2, timestamp):
		try:
			db = firebase.database()
			storage = firebase.storage()
			filename = self.format_filename(name, timestamp)

			imgpath = os.path.join(fileDir, img_1)
			filename1 = filename + '_a.jpg'
			storage.child("visitors").child(filename1).put(imgpath)
			img1url = storage.child("visitors").child(filename1).get_url(None)
			
			imgpath = os.path.join(fileDir, img_2)
			filename2 = filename + '_b.jpg'
			storage.child("visitors").child(filename2).put(imgpath)
			img2url = storage.child("visitors").child(filename2).get_url(None)

			userdata = {"img1": img1url, "img2": img2url, "isCompleted": False, "name": name, "ts": timestamp, "user": "", "userUID": "", "comment": ""}
			db.child("visitors").push(userdata)

			logdata = {"visitor": name, "event": "ARRIVED", "ts": timestamp}
			db.child("eventlog").push(logdata)

		except Exception as e:
			print("Failed to save images")
			print(e)
			return

	def format_filename(self, name, timestamp):
		#given DD/MM/YY HH:MM:SS, format will be YYMMDDHHMMSS
		file_name = name + '/'
		file_name += timestamp[6:8] #year
		file_name += timestamp[3:5] #month
		file_name += timestamp[:2]  #day
		file_name += timestamp[9:11] #hour
		file_name += timestamp[12:14] #min
		file_name += timestamp[15:]  #sec

		return file_name
