# -*- coding: utf-8 *-*
"""
Core library for handling slow query logs with Solr.
"""

import urlparse

class LogHandler(object):
    
     def __init__(self):
         # obv needs to get mongo DI in hurr
         pass

     """
     Given a log line, introduce logic for storing info
     """
     def handle(self, line):
         line = LogLine(line)
         print line.getTimestamp(), line.get(u'QTime'), line.getParams().get(u'q', u'')


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
