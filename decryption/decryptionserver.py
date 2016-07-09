__author__ = 'wali'

from flask import Flask,request
from pymongo import MongoClient
import json
from flask import render_template
app = Flask(__name__, static_url_path="/static")

# Global
dataBase = None
documentCursor = None
currentDocumentCursorCount = 0
collectionList = None
currentCollectionCursorCount = 0

def getNextDocument():
    global currentDocumentCursorCount
    global documentCursor
    if(documentCursor is None or currentDocumentCursorCount >= documentCursor.count()):
        documentCursor = getNextDocumentCursor()
    try:
        documentToReturn = documentCursor[currentDocumentCursorCount]
        currentDocumentCursorCount = currentDocumentCursorCount + 1
        print "Current count is now " + str(currentDocumentCursorCount)
        del documentToReturn[u"_id"]
        return json.dumps(documentToReturn)
    except:
        return "---End---"

def getNextDocumentCursor():
    global currentCollectionCursorCount
    if (currentCollectionCursorCount >= len(collectionList)):
        return None
    documentCursorToReturn = dataBase[collectionList[currentCollectionCursorCount]].find()
    print "Count is " + str(documentCursorToReturn.count())
    currentCollectionCursorCount == currentCollectionCursorCount + 1
    return documentCursorToReturn

@app.route('/decryptpage/',)
def serveHTMLPage():
    return render_template('decrypt.html')

@app.route('/getDocument',methods = ['GET','POST'])
def sendDocument():
    return getNextDocument()



@app.route('/depositDocument',methods = ['POST'])
def receiveDocument():
    print request.json
    return "Thanks"

if __name__ == '__main__':
    mongoClient = MongoClient()
    dataBase = mongoClient['user_encrypted_data']
    collectionList = dataBase.collection_names()
    print collectionList
    app.run(host='127.0.0.1',debug=True,use_reloader=False, port=int("7080"))