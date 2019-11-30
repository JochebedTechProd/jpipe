import mysql.connector
import json
import sys
#from .snippets import callSnippet
import snippets
#global callingDb
'''
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}',None)
'''
callingDb = mysql.connector.connect(
    host="localhost",
    user="jpipe",
    passwd="jpipe",
    database="JpipeDB")
print '##############################################################################'
print '{"userid":"admin1","jsonStrKey":"V","fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","jsonStrKey":"V","fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}',callingDb)
'''
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"V","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"V","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"14"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","minVal":"0","maxVal":"14"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","minVal":"0","maxVal":"14"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","maxVal":"14"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","maxVal":"14"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","minVal":"12"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","minVal":"0"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","jsonStrKey":"V"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","jsonStrKey":"V"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","jsonStrKey":"B"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","jsonStrKey":"B"}',callingDb)
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":"charge","fromDate":"2019-07-03 00:00","maxVal":"0"}'
snippets.callSnippet("fieldSummary",'{"userid":"admin1","devId":"2","jsonStrKey":"charge","fromDate":"2019-07-03 00:00","maxVal":"0"}',callingDb)
'''
print '##############################################################################'
print '{"userid":"admin1","devId":"2","jsonStrKey":["V","charge"],"fromDate":"2019-07-05 20:00"}'
snippets.callSnippet("graphData",'{"userid":"admin1","devId":"2","jsonStrKey":["V","charge"],"fromDate":"2019-07-05 15:30"}',callingDb)
