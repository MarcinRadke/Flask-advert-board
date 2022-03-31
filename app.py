from ast import Add
from flask import Flask, render_template, request, jsonify
import flask
import json
from advert import Advert
from repository import Repository
import datetime
import sqlite3

app = Flask(__name__)

repository = Repository()

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('advert.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/")
def hello_world():
    headers = request.headers.get('Authorization')
    return "Request headers:\n" + str(headers)

@app.route("/about")
def about():
    return 'Advert board using flask'

@app.route("/create", methods =['POST'])
def create():
    conn = db_connection()
    cursor =  conn.cursor()
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    jsonr = request.json

    sql_check_title = """ SELECT title FROM advert WHERE title = ?"""

    cursor.execute(sql_check_title, (jsonr['title'],))
    answer = cursor.fetchone()

    if answer != None:
        return "Title already exist", 400

    # all_advertise = repository.advert_list
    # title_names = []

    # for title in all_advertise:
    #     title_names.append(title['title'])
    #     if jsonr['title'] in title_names:
    #         return "Title already exists", 400

    # advert = Advert(date_time, date_time, jsonr['title'], jsonr['details'], jsonr['email'], request.headers.get('Authorization'))
    # dictadvert = (advert.__dict__)
    # repository.advert_list.append(dictadvert)
    # return  json.dumps(dictadvert)

    sql = """INSERT INTO advert (creation_date, update_date, title, details, email, author_login)
            VALUES (?, ?, ?, ?, ?, ?)"""
    cur = cursor.execute(sql, (date_time, date_time, jsonr['title'], jsonr['details'], jsonr['email'], request.headers.get('Authorization')))
    conn.commit()
    return f"Advert with the id: {cur.lastrowid} created successfully", 200

@app.route("/update", methods =['PUT'])
def update():
    conn = db_connection()
    cursor =  conn.cursor()
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    # all_advertise = repository.advert_list
    # title_names = []
    # usernames = []
    jsonr = request.json

    sql_check_title = """ SELECT title FROM advert WHERE title = ?"""

    cursor.execute(sql_check_title, (jsonr['title'],))
    title = cursor.fetchone()

    if title == None:
        return "Title doesn't exist", 400

    sql_check_username = """ SELECT author_login FROM advert WHERE title = ?"""

    cursor.execute(sql_check_username, (jsonr['title'],))
    username = cursor.fetchone()

    if request.headers.get('Authorization') != username[0] and request.headers.get('Authorization') != 'admin':
        return "You can't change not your advertisment", 400

    sql_change = """ UPDATE advert
                    SET details=?
                    WHERE title=?"""

    conn.execute(sql_change, (jsonr['details'], jsonr['title']))
    conn.commit()

    return "Changed " + jsonr['title']

    # for title in all_advertise:
    #     title_names.append(title['title'])
    
    # for author_login in all_advertise:
    #     usernames.append(author_login['author_login'])

    # if jsonr['title'] not in title_names:
    #     return "Title doesn't exist", 400

    # if request.headers.get('Authorization') != usernames[title_names.index(jsonr['title'])] and request.headers.get('Authorization') != 'admin':
    #     return "You can't change not your advertisment", 400

    # new_json = all_advertise[title_names.index(jsonr['title'])]

    # new_json['details'] = jsonr['details']
    # new_json['update_date'] = date_time

    # all_advertise[title_names.index(jsonr['title'])] = new_json
    
    # return "Changed " + jsonr['title']

@app.route("/delete", methods =['DELETE'])
def delete():
    conn = db_connection()
    cursor =  conn.cursor()
    # all_advertise = repository.advert_list
    # title_names = []
    # usernames = []
    jsonr = request.json

    sql_check_title = """ SELECT title FROM advert WHERE title = ?"""

    cursor.execute(sql_check_title, (jsonr['title'],))
    title = cursor.fetchone()

    if title == None:
        return "Title doesn't exist", 400

    sql_check_username = """ SELECT author_login FROM advert WHERE title = ?"""

    cursor.execute(sql_check_username, (jsonr['title'],))
    username = cursor.fetchone()

    if request.headers.get('Authorization') != username[0] and request.headers.get('Authorization') != 'admin':
        return "You can't delete not your advertisment", 400
    
    sql_delete = """ DELETE FROM advert WHERE title=?"""
    conn.execute(sql_delete, (jsonr['title'],))
    conn.commit()

    return "Deleted " + jsonr['title']

    # for title in all_advertise:
    #     title_names.append(title['title'])

    # for author_login in all_advertise:
    #     usernames.append(author_login['author_login'])
    
    # if jsonr['title'] not in title_names:
    #     return "Title doesn't exist", 400

    # if request.headers.get('Authorization') != usernames[title_names.index(jsonr['title'])] and request.headers.get('Authorization') != 'admin':
    #     return "You can't delete not your advertisment", 400

    # all_advertise.pop(title_names.index(jsonr['title']))
    
    # return 'Deleted ' + jsonr['title']\

@app.route("/all")
def all():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM advert")
    adverts = [
        dict(id=row[0], creation_date=row[1], update_date=row[2], title=row[3], details=row[4], email=row[5], author_login=row[6])
        for row in cursor.fetchall()
    ]
    if adverts is not None:
        return jsonify(adverts)
    
    #all_advertise = repository.advert_list
    #return json.dumps(all_advertise)

if __name__ == '__main__':
    app.run(debug=True)