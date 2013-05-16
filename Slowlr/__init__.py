# -*- coding: utf-8 *-*
"""
Core library for handling slow query logs with Solr.
"""

import urlparse, datetime
from pymongo import MongoClient

class LogHandler(object):
    
     def __init__(self):
          #todo: config port and host
          self.client = MongoClient()
          self.db = self.client.slowlr
          self.slowQTime = 100 #todo: configurable

     """
     Given a log line, introduce logic for storing info
     """
     def handle(self, line):
         line = LogLine(line)
         qtime = line.get(u'QTime')
         #note we assume log emissions are real-time
         if qtime >= self.slowQTime:
              self.db.queries.insert({
                   u'query' : line.getParams().get(u'q', u''),
                   u'timestamp' : datetime.datetime.utcnow(),
                   u'qtime' : int(qtime),
                   u'hits' : int(self.get('hits', 0))
              })
         print line.getTimestamp(), qtime, line.getParams().get(u'q', u'')


class LogLine(object):

    def __init__(self, line):
        self.lineData = line.split(u' ')
        self.timestamp = self.lineData[0]
        #e.g. INFO:, so [:-1]
        self.logLevel = self.lineData[1][:-1]
        #e.g. [main]
        self.core = self.lineData[2][1:-1]
        self.keyVals = {}
        for grouping in self.lineData[3:]:
            [key, value] = [grouping.split(u'=')[0], u'='.join(grouping.split(u'=')[1:])]
            self.keyVals[key] = value

    def get(self, key):
        return self.keyVals.get(key, False)

    def getParams(self):
        return urlparse.parse_qs(self.get(u'params')[1:-1])

    def getTimestamp(self):
        return self.timestamp
