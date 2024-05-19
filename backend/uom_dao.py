from sql_connection import getSqlConnection


def getUOM(mydb):
    cursor=mydb.cursor()
    cursor.execute("SELECT * from units")
    response = []
    for (uom_id, unit) in cursor:
        response.append({
        'uom_id': uom_id,
        'unit': unit
    })
    return response

if __name__ == '__main__':
    mydbconn=getSqlConnection()
    print(getUOM(mydbconn))