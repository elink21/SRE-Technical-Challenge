import mysql.connector
import hashlib


from mysql.connector import Error

try:
    connection = mysql.connector.connect(host="bootcamp-tht.sre.wize.mx", database="bootcamp_tht",
                                         user="secret", password="noPow3r")
    if(connection.is_connected()):
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select password from users where username='admin'")
        record = cursor.fetchall()
        for row in record:
            print(row)
except Error as e:
    print("Error while connecting", e)
finally:
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection closed")
