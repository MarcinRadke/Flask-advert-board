from ast import Add
from flask import Flask, render_template, request
import flask
import json
from advert import Advert
from repository import Repository
import datetime
import sqlite3

app = Flask(__name__)

repository = Repository()

@app.route("/")
def hello_world():
    headers = request.headers.get('Authorization')
    return "Request headers:\n" + str(headers)

@app.route("/about")
def about():
    return 'Advert board using flask'

@app.route("/create", methods =['POST'])
def create():
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    jsonr = request.json
    all_advertise = repository.advert_list
    title_names = []

    for title in all_advertise:
        title_names.append(title['title'])
        if jsonr['title'] in title_names:
            return "Title already exists", 400

    advert = Advert(date_time, date_time, jsonr['title'], jsonr['details'], jsonr['email'], request.headers.get('Authorization'))
    dictadvert = (advert.__dict__)
    repository.advert_list.append(dictadvert)
    return  json.dumps(dictadvert)

@app.route("/update", methods =['PUT'])
def update():
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    all_advertise = repository.advert_list
    title_names = []
    usernames = []
    jsonr = request.json

    for title in all_advertise:
        title_names.append(title['title'])
    
    for author_login in all_advertise:
        usernames.append(author_login['author_login'])

    if jsonr['title'] not in title_names:
        return "Title doesn't exist", 400

    if request.headers.get('Authorization') != usernames[title_names.index(jsonr['title'])] and request.headers.get('Authorization') != 'admin':
        return "You can't change not your advertisment", 400

    new_json = all_advertise[title_names.index(jsonr['title'])]

    new_json['details'] = jsonr['details']
    new_json['update_date'] = date_time

    all_advertise[title_names.index(jsonr['title'])] = new_json
    
    return "Changed " + jsonr['title']

@app.route("/delete", methods =['DELETE'])
def delete():
    all_advertise = repository.advert_list
    title_names = []
    usernames = []
    jsonr = request.json

    for title in all_advertise:
        title_names.append(title['title'])

    for author_login in all_advertise:
        usernames.append(author_login['author_login'])
    
    if jsonr['title'] not in title_names:
        return "Title doesn't exist", 400

    if request.headers.get('Authorization') != usernames[title_names.index(jsonr['title'])] and request.headers.get('Authorization') != 'admin':
        return "You can't delete not your advertisment", 400

    all_advertise.pop(title_names.index(jsonr['title']))
    
    return 'Deleted ' + jsonr['title']

@app.route("/all")
def all():
    all_advertise = repository.advert_list
    return json.dumps(all_advertise)

if __name__ == '__main__':
    app.run(debug=True)