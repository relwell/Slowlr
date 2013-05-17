from flask import Flask, render_template, jsonify, request
from flask.ext.pymongo import PyMongo
from bson import Code
from bson.json_util import dumps

app = Flask('slowlr')
mongo = PyMongo(app)

app.debug = True
limit = 25

@app.route(u'/')
def home_page():
    return render_template(u'index.html')

@app.route(u'/_page/<page>')
def get_page(page):
    offset = (int(page) -1) * limit
    currlimit = offset + limit
    mf = Code(u"""function() { var q = this.query; this.instances.forEach(function(z) { emit( q, z.qtime ); } ) }""")
    rf = Code(u"""rf = function( key, vals ) { parseFloat(Array.sum(vals))/parseFloat(vals.length); }""")
    mongo.db.queries.map_reduce(mf, rf, u"avg_slow_queries")
    results = mongo.db.avg_slow_queries.find().sort(u'value', -1)
    slow_queries = [{u'qtime':instance[u'value'], u'query':instance[u'_id']} for instance in results[offset:currlimit]]
    return jsonify({u'queries':slow_queries})

@app.route(u'/_query/', methods=['POST'])
def inspect_query():
    query = request.form.get('query', '')
    return dumps(mongo.db.queries.find_one({'query':query}))

app.run()
