import mysql.connector
import backend.importData.get_all_product as allP

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="373600",
  database="test1"
)

mycursor = mydb.cursor()

sql = 'INSERT INTO no_season_product (productName, brandLogo, brandName, productCategory, colorShade, productImage, productDescription) VALUES (%s, %s, %s, %s, %s, %s, %s)'
val = allP.show_product()

mycursor.executemany(sql, val)

mydb.commit()

print("1 record inserted, ID:", mycursor.lastrowid)