# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import csv
import datetime as dt

class sql():
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    def create_table(self, conn):
        try:
            conn.execute("DROP TABLE IF EXISTS outcomes;")
        except:
            print("Error in Table Drops")

        sql_str = '''
            CREATE TABLE outcomes(
                county TEXT,
                zip INT,
                month TEXT,
                junction INT,
                weekday TEXT,
                temperature INT,
                state TEXT,
                predictionHT REAL,
                countyMedian REAL,
                zipMedian REAL,
                accidentsNumber INT
            )
        '''
        return self.execute_query(conn, sql_str)

    def insert_data(self, conn, path):
        with open(path,newline='',encoding = 'utf8',errors = 'ignore') as file:
            lines = csv.reader(file)
            next(lines)
            for line in lines:
                line[3] = 0 if line[3] == 'False' else 1
                sql_str = "INSERT INTO outcomes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                cursor = conn.execute(sql_str,(str(line[0]), int(line[1]), str(line[2]), int(line[3]), str(line[4]), int(line[5]), str(line[6]), float(line[7]), float(line[8]), float(line[9]), int(line[10])))
        conn.commit()
        sql_str = "SELECT COUNT(*) FROM outcomes"
        cursor = conn.execute(sql_str)
        return cursor.fetchall()[0][0]

    def get_ht(self, conn):
        sql_str = "SELECT DISTINCT county, countyMedian, accidentsNumber, state FROM outcomes WHERE state <> ''"
        cursor = conn.execute(sql_str)
        return cursor.fetchall()

    def query_ht(self, conn, zipcode = 00000, date = '2020-1-9', junction = 0, temperature = 20):
        date = dt.datetime.strptime(date,"%Y-%m-%d")
        day_of_week = date.strftime("%A")[:3]
        month = date.strftime('%b')
        temp = 0 if temperature >= 39 else 1
        sql_str = """
            SELECT zip, county, predictionHT, state
            FROM outcomes
            WHERE zip = ? AND month = ? AND junction = ? AND weekday = ? AND temperature = ?
            LIMIT 1
            """
        cursor = conn.execute(sql_str, (zipcode, month, junction, day_of_week, temp))
        return cursor.fetchall()

    def query_zip_ht(self, conn, zipcode):
        sql_str = """
            SELECT zip, county, zipMedian, state
            FROM outcomes
            WHERE zip = ?
            LIMIT 1
        """
        cursor = conn.execute(sql_str, (zipcode,))
        return cursor.fetchall()

if __name__ == "__main__":
    db = sql()
    try:
        conn = db.create_connection("team97")
    except:
        print("Database Creation Error.")

    try:
        res = db.create_table(conn)
        print("Create table: "+ str(res))
    except:
        print('Create table error.')

    try:
        res = db.insert_data(conn, "outcome_processed_111120.csv")
        print("Insert data: " + str(res))
    except:
        print("Insert data error.")
    try:
        cursor = conn.execute("SELECT * FROM outcomes Where zip = ? and month = ? LIMIT 5", (1001,'Jan'))
        lines = cursor.fetchall()
        for line in lines:
            print(line)
    except:
        print("Query HT 5 error.")

    try:
        res = db.query_zip_ht(conn, 1001)
        print("query result for zip HT:" + str(res))
    except:
        print("Query zip HT error.")

    try:
        res = db.query_ht(conn, zipcode = 1001, date = '2020-1-9', junction = 0, temperature = 80)
        print("query result for HT:" + str(res))
    except:
        print("Query HT error.")

    try:
        res = db.get_ht(conn)
        print("Get result for HT:" + str(res))
    except:
        print("Get HT error.")


    conn.close()
