from flask import Flask, render_template, jsonify
from flask.ext.pymongo import PyMongo

app = Flask('slowlr')
mongo = PyMongo(app)

app.debug = True
limit = 25

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/_page/<page>')
def get_page(page):
    offset = (int(page) -1) * limit
    currlimit = offset + limit
    slow_queries = [{'qtime':instance['qtime'], 'query':instance['query'], 'hits':instance.get('hits', 0)} for instance in mongo.db.queries.find().sort('qtime', -1)[offset:currlimit]]
    return jsonify({'queries':slow_queries})

app.run()
