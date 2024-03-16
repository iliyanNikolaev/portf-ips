import mysql.connector

def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ips_db',
            user='root',
            password='123456qwerty'
        )
        return connection
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

conn = connect()

def fetch_survey_data():
    if not conn:
        return None
    
    query = 'SELECT * FROM survey_data'
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = {}
            for i, value in enumerate(row):
                result[columns[i]] = value
            results.append(result)
        return results
    except mysql.connector.Error as error:
        print("Error while fetching data from MySQL", error)
        return None
    finally:
        if cursor:
            cursor.close()