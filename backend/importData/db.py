import mysql.connector
import backend.importData.get_all_product as allP

# Database connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="373600",
    database="test1"
)
mycursor = mydb.cursor()

def chunk_data(data, chunk_size):
    """Split data into smaller chunks."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def validate_product_data(data):
    """Ensure all items are tuples with 8 elements."""
    for item in data:
        if not isinstance(item, tuple) or len(item) != 8:
            print(f"Invalid product data: {item}")
            return False
    return True

def update_data():
    """Insert product data in chunks."""
    sql = '''
        INSERT INTO product1 (productName, brandLogo, brandName, productCategory, 
                             colorShade, productImage, productDescription, seasonColorTone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            brandLogo=VALUES(brandLogo), 
            productImage=VALUES(productImage),
            productDescription=VALUES(productDescription)
    '''
    val = allP.get_product()

    if not validate_product_data(val):
        print("Aborting insert due to invalid product data.")
        return

    for chunk in chunk_data(val, 50):
        try:
            mycursor.executemany(sql, chunk)
            mydb.commit()
            print(f"{mycursor.rowcount} records inserted/updated.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            mydb.rollback()

def clear_table():
    """Clear product table and reset AUTO_INCREMENT."""
    try:
        mycursor.execute("DELETE FROM product1")
        mycursor.execute("ALTER TABLE product1 AUTO_INCREMENT = 1")
        mydb.commit()
        print("Table cleared.")
    except mysql.connector.Error as err:
        print(f"Error clearing table: {err}")
        mydb.rollback()

if __name__ == "__main__":
    clear_table()
    update_data()
    mycursor.close()
    mydb.close()
