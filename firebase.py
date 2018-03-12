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
			traceback.print_exc()
			return

	def getDBcourses(self, course, professor):
		try:
			if (professor is None):
                                return "A99", "T"	
			else:
				db = firebase.database()
				course_data = db.child("courses").child(course).child("professors").child(professor).get().val()
				return course_data['classroom'], course_data['period']

		except Exception as e:
			print(e)
			traceback.print_exc()
			return
