import time
import math
import sqlite3
from flask import url_for

class FDataBase:
	def __init__(self, db):
		self.__db=db
		self.__cur=db.cursor()


	def getPost(self, username, password):
		try:
			#self.__cur.execute(f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}' LIMIT 1")
			self.__cur.execute(f"SELECT id FROM users WHERE username = '%s' AND password = '%s' LIMIT 1" % (username, password))
			res = self.__cur.fetchone()
			if res:
				#base = url_for('static', filename='images_html')
				#text = res.sub(r"")
				#return res
				return True
		except:
			#print("Ошибка получения статьи из бд"+str(e))
			return False


	def addPost(self, username, password):
		try:
			# self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE	username LIKE '{username}'")
			# res = self.__cur.fetchone
			# if int(res['count']) > 0:
			# 	return False

			self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?)", (username,password, "Permission denied"))
			self.__db.commit()
		except sqlite3.Error as e:
			print('Ошибка добавления')
			return False
		return True


	def getUser(self, user_id):
		try:
			self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
			res = self.__cur.fetchone()
			if not res:
				return False
			return res
		except:
			print("some error")
		return False


	def getUserByEmail(self, username):
		try:
			self.__cur.execute(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1")
			res = self.__cur.fetchone()
			if not res:
				return False
			return res
		except sqlite3 as e:
			print('some error')
		return False

