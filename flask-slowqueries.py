from flask import Flask, render_template
from flask.ext.pymongo import PyMongo

app = Flask('slowlr')
mongo = PyMongo(app)

app.debug = True

@app.route('/')
def home_page():
    slow_queries = mongo.db.queries.find().sort('qtime', -1)
    return render_template('index.html', slow_queries=slow_queries)

app.run()
