from sql_connection import getSqlConnection

def getAllProducts(mydb):
    cursor=mydb.cursor()
    cursor.execute("SELECT products.product_id, products.name, products.uom_id,products.price_per_unit, units.unit FROM products inner join units on units.uom_id=products.uom_id")
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
        'product_id': product_id,
        'name': name,
        'uom_id': uom_id,
        'price_per_unit': price_per_unit,
        'uom_name' : uom_name
    })
    return response

def addProduct(mydb,newProduct):
    cursor=mydb.cursor()
    query="insert into products (name, uom_id,price_per_unit) VALUES (%s, %s ,%s)"
    data=(newProduct['product_name'], newProduct['uom_id'],newProduct['price_per_unit'])
    cursor.execute(query,data)
    mydb.commit()
    return cursor.lastrowid

def deleteProduct(mydb,productId):
    cursor=mydb.cursor()
    query = ("DELETE FROM products where product_id=" + str(productId))
    cursor.execute(query)
    mydb.commit()
    return cursor.lastrowid



if __name__ == '__main__':
    mydbconn=getSqlConnection()
    print(getAllProducts(mydbconn))
    # print(addProduct(mydbconn,{
    #     'product_name':'Brocalli',
    #     'uom_id':2,
    #     'price_per_unit':40
    # }))
    print(deleteProduct(mydbconn,6))
