import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="YourPasswordHere",
        database="FoodDeliveryDB",
        cursorclass=pymysql.cursors.Cursor
    )
