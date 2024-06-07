import mysql.connector

connect_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="099*3941115",
    database="test_flask",
)

def get_data():
    cursor = connect_db.cursor()
    cursor.execute("SELECT * FROM product")
    result = cursor.fetchall()
    cursor.close()
    return result


