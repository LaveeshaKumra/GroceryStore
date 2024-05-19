import mysql.connector

__cnx=None
def getSqlConnection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="groceryStoreProject"
        )
    return __cnx
