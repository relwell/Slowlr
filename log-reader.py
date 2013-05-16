"""
This is a log handler in built using the Unix philosophy.
This takes log lines from stdin and directs them to Slowlr's log handler.
To start logging, you should invoke tail -F $MY_LOGFILE | python log-reader.py
Since we specifically care about slow query logging here, 
you could also do tail -F $MY_LOGFILE | grep QTime | python log-reader.py to improve performance and coverage.
"""

import sys, codecs
from Slowlr import LogHandler

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

handler = LogHandler()

counter = 0
for line in codecs.getreader('utf-8')(sys.stdin):
    # All logic is inside the handler class (as it damn well should be)
    handler.handle(line)
    counter += 1
