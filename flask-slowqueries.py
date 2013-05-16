from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def home_page():
    slow_queries = mongo.db.users.find({'online': True}).sort({'qtime':-1})
    return render_template('index.html', slow_queries=slow_queries)

app.run()
