from datetime import datetime
from sql_connection import getSqlConnection

def insertOrder(mydb,order):
    cursor=mydb.cursor()
    query="insert into orders (customer_name, total_order_value,date_of_purchase) VALUES (%s, %s ,%s)"
    data=(order['customer_name'], order['grand_total'],datetime.now())
    cursor.execute(query,data)
    orderid= cursor.lastrowid

    order_details_query = ("INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
    order_details_data = []
    for order_detail_record in order ['order_details']:
        order_details_data.append( [
        orderid,
        int (order_detail_record['product_id']),
        float(order_detail_record['quantity']),
        float(order_detail_record['total_price'])
        ])
    cursor.executemany (order_details_query, order_details_data)
    mydb.commit()
    return orderid

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from order_details where order_id = %s"

    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
            "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response



if __name__ == '__main__':
    mydbconn=getSqlConnection()
    print(insertOrder(mydbconn, {
    "customer_name": "dhaval",
    "grand_total": "500",
    "date_of_purchase":datetime.now(),
    "order_details": [
        {
            "product_id": 1,
            "quantity": 2,
            "total_price": 50
        },
        {
            "product_id": 3,
            "quantity": 1,
            "total_price": 30
        }
    ]
}))
    