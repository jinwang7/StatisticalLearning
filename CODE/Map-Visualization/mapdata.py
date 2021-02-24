# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, g
import json
import database
import sqlite3

db = database.sql()


def loadDB():
    try:
        conn = db.create_connection("m97")
    except:
        print(" * Database Creation Error.")

    try:
        res = db.create_table(conn)
        print(" * Create table: " + str(res))
    except:
        print(' * Create table error.')

    try:
        res = db.insert_data(conn, "outcome_processed_111220.csv")
        print(" * Insert data: " + str(res))
    except:
        print("Insert data error.")
    conn.close()


def createApp():
    print(" * Loading data....")
    loadDB()
    print(" * Data is Loaded into DB.")
    return Flask(__name__)


app = createApp()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getMapData')
def getMapData():
    data = readData()
    return jsonify(data)


@app.route("/getCountyData")
def getCountyData():
    data = readCountyData()
    return jsonify(data)


@app.route('/getHTData')
def getHTData():
    args = request.args
    # get all Handeling Time
    if len(args) == 0:
        return jsonify(getAllHT())

    zipcode = int(args.get('zip'))
    date = str(args.get('date'))
    junction = int(args.get('junction'))
    temperature = int(args.get('temperature'))

    return jsonify(queryHT(zipcode, date, junction, temperature))


def readData():
    with open('us.json') as f:
        data = json.load(f)
    return data


def readCountyData():
    with open('county.json') as f:
        data = json.load(f)
    return data


def getAllHT():
    try:
        conn = sqlite3.connect('m97')
    except Exception as e:
        print(str(e))
    data = db.get_ht(conn)
    conn.close()
    res = []
    for x in data:
        res.append({'county': x[0], 'countyMedianHT': x[1],
                    'accidentNum': x[2], 'state': x[3]})
    return res


def queryHT(zipcode, date, junction, temperature):
    try:
        conn = sqlite3.connect('m97')
    except Exception as e:
        print(str(e))
    data = db.query_ht(conn, zipcode, date, junction, temperature)
    if not data:
        data = db.query_zip_ht(conn, zipcode)
    conn.close()
    res = {'zip': data[0][0], 'county': data[0]
           [1], 'HT': data[0][2], 'state': data[0][3]}
    return res


if __name__ == "__main__":
    app.run(debug=False)
