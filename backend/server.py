from flask import Flask, request, jsonify ,json
from flask_cors import CORS
import products_dao,uom_dao,orders_dao,sales_dao
from sql_connection import getSqlConnection

#####
from datetime import datetime

app = Flask (__name__)

mydbconn=getSqlConnection()
@app.route('/getProducts')
def getProducts():
    products= products_dao.getAllProducts(mydbconn)
    response= jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route('/getUOM',methods=['GET'])
def getUOM():
    uom=uom_dao.getUOM(mydbconn)
    response= jsonify(uom)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads (request.form['data'])
    product_id = products_dao.addProduct(mydbconn, request_payload)
    response = jsonify({
    'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct',methods=['POST'])
def deleteProduct():
    product_id = products_dao.deleteProduct(mydbconn,request.form['product_id'])
    response = jsonify({
    'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(mydbconn)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insertOrder(mydbconn, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response






@app.route('/getDailySales', methods=['POST'])
def getDailySales():
    request_payload = json.loads(request.form['data'])
    sales = sales_dao.fetch_sales_data(mydbconn,request_payload)
    response= jsonify(sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000,debug=True)