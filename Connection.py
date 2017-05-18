import MySQLdb

def get_connection():
	db = MySQLdb.Connect(host="localhost", port=3366, user="root", passwd="")
	cursor = db.cursor()
	db.autocommit(True)
	return db,cursor

def close_connection(cursor,db):
	cursor.close()
	db.close()	