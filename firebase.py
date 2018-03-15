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

		##Uncomment for individual use##
		"""
		course = "Finanzas 2"
		parallels = self.get_DB_course_parallels(course)
		print(("Existen {} paralelos de {}...").format(len(parallels), course))
		for parallel in parallels:
			professor = parallel['professor']
			classroom = parallel['classroom']
			period = parallel['period']
			print(("{}. Las clases son en {} en horario {}").format(professor, classroom, period))
		"""

	def connect(self):
		try:
			print("Connecting...")
			global firebase
			firebase = pyrebase.initialize_app(fireconfig)
			print("Connected to DB: " + fireconfig["databaseURL"])
		except Exception as e:
			print("Failed connection to DB!")
			print(e)
			return

	def get_DB_course_parallels(self, course = None):
		try:
			db = firebase.database()
			course_data = db.child("courses").child(course).child("parallels").get().val()
			return course_data

		except Exception as e:
			print(e)
			return

##Uncomment for individual use##
"""
if __name__ == "__main__": 
	firebase = Firebase()
"""