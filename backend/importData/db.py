import mysql.connector
import backend.importData.get_all_product as allP

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="373600",
  database="test1"
)

mycursor = mydb.cursor()

def update_data():
  clear_table()
  sql = 'INSERT INTO product (productName, brandLogo, brandName, productCategory, colorShade, productImage, productDescription, colorTone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
  val = allP.get_product()
  mycursor.executemany(sql, val)

  mydb.commit()
  print("1 record inserted, ID:", mycursor.lastrowid)

def clear_table():
  sql = "DELETE FROM no_season_product"
  reset_sql = "ALTER TABLE no_season_product AUTO_INCREMENT = 1"
  try:
    # Execute the SQL command
    mycursor.execute(sql)
    mycursor.execute(reset_sql)
    # Commit your changes in the database
    mydb.commit()
  except:
    mydb.rollback()


update_data()

mycursor.close()
mydb.close()