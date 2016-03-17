__author__ = 'wali'

from flask import Flask, request
from pymongo import MongoClient
from detection_system import detection_system
from histo import histo_detection


def check_for_null_session(collection,entry):
    if (collection.find({'SessionKey': entry['SessionKey']}).count() is 1 and entry['ActionSubClass'] == 'CloseTab'):
        print "Null Session Detected"
        collection.remove({'SessionKey': entry['SessionKey']})
        return True
    return False

def add_to_Log(request):
    if request.headers['Content-Type'] == 'application/json':
        print request.json
        c_k = request.json['ClientKey']
        clientCollection = dataBase[c_k]
        for entry in request.json['Events']:
            #Sending Event to Detection System
            try:detection_system.new_entry(entry,c_k,True,True)
            except: print "Detection System Failure"

            #Checking for Empty Session
            if(check_for_null_session(clientCollection,entry)):
                continue
            clientCollection.insert_one(entry)
    return "Logged"


app = Flask(__name__)

#Global Variables
detection_system = histo_detection()
dataBase = None

@app.route('/')
def api_root():
    return 'Welcome'

# Method takes JSON array of log objects
    # Single item will be an array of length 1
    # Mutliple items will be an array of length 'n'
@app.route('/submit', methods = ['POST'])
def api_submit():
    return add_to_Log(request)

#### COMMAND LINE ARUGMENTS ####

if __name__ == '__main__':
    mongoClient = MongoClient()

    #Select Mongo DB to use
    dataBase = mongoClient['mydb']

    #If Detection System Does Not Store Data, Call this to feed it past data
    try:detection_system.load_from_database(dataBase)
    except: print "Detection System Failure"

    #Start Flask Server
    app.run(host='0.0.0.0',debug=True)

