import mysql.connector
connect = mysql.connector.connect(user="MK", password="6860",
                                  host="127.0.0.1",
                                  database="bvtc")

try:
    cursor = connect.cursor()
    cursor.execute("""
    select * from bvtc.blocks
    
    """)
    result = cursor.fetchall()
    print(result)
finally:
    connect.close()
