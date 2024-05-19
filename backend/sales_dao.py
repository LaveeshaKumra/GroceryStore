from sql_connection import getSqlConnection

def fetch_sales_data(conn,data):
    cursor = conn.cursor()
    query = "SELECT  DATE(date_of_purchase) AS purchase_date, COUNT(*) AS total_orders, SUM(total_order_value) AS total FROM orders  WHERE  YEAR(date_of_purchase) = %s AND MONTH(date_of_purchase) = %s GROUP BY  DATE(date_of_purchase);"
    cursor.execute(query, (data['year'], data['month']))
    response = []
    for (purchase_date, total_orders, total) in cursor:
        response.append({
        'purchase_date': purchase_date,
        'total_orders': total_orders,
        'total': total
    })
    return response

if __name__ == '__main__':
    mydbconn=getSqlConnection()
    data={
        "year":2024,
        "month":5
    }
    print(fetch_sales_data(mydbconn,data))
    