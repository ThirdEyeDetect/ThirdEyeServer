__author__ = 'wali'

from flask import Flask, request
from flask import render_template
from pymongo import MongoClient
from detection_system import detection_system
from place_holder_system import placeholder

#Global Variables
detection_system = None
dataBase = None


def check_for_null_session(collection,entry):
    if (collection.find({'SessionKey': entry['SessionKey']}).count() is 1 and entry['ActionSubClass'] == 'CloseTab'):
        print "Null Session Detected"
        collection.remove({'SessionKey': entry['SessionKey']})
        return True
    return False

def add_to_Log(request):
    if request.headers['Content-Type'] == 'application/json':
        print request.json
        c_i = request.json['ClientID']
        clientCollection = dataBase[c_i]
        for entry in request.json['Events']:
            #Sending Event to Detection System
            try:detection_system.new_entry(entry,c_i,True,True)
            except Exception as Error: print "Detection System Failure: " + repr(Error)

            #Checking for Empty Session
            if(check_for_null_session(clientCollection,entry)):
                continue
            clientCollection.insert_one(entry)
    return "Logged"


app = Flask(__name__)

@app.route('/')
def api_root():
    return render_template('welcomepage.html')

# Method takes JSON array of log objects
    # Single item will be an array of length 1
    # Mutliple items will be an array of length 'n'
@app.route('/submit', methods = ['POST'])
def api_submit():
    return add_to_Log(request)

@app.route('/email',methods = ['POST'])
def api_email():
    if request.headers['Content-Type'] == 'application/json':
        print request.json
        mongoClient2 = MongoClient()
        dataBase2 = mongoClient2['client_to_email']
        dataBase2['emails'].insert_one(request.json)
        try:detection_system.alarm(request.json['ClientID'],'Extension installation success',"The ThirdEye extension was successfully installed on Chrome.")
        except Exception as error: print "Detection System Failure: " + repr(error)
        return "success"
    return "failed"

@app.route('/uninstall',methods= ['GET'])
def api_uninstall():
    id = request.args.get('id')
    if not id:
        return "You did not set a communication channel"
    try:detection_system.alarm(id,'Extension was uninstalled',"Third Eye was uninstalled from Chrome")
    except Exception as error: print "Detection System Failure: " + repr(error)
    return "Thank you"



if __name__ == '__main__':
    mongoClient = MongoClient()

    #Select Mongo DB to use
    dataBase = mongoClient['user_encrypted_data']

    #Select Detection System
    #detection_system = mdp_variant()

    #Place Holder
    detection_system = placeholder()

    #If Detection System Does Not Store Data, Call this to feed it past data
    #try:detection_system.load_from_database(dataBase)
    #except Exception as Error: print "Detection System Failure: " + repr(Error)

    #Start Flask Server
    context = ('thirdeye_server_cert.crt','thirdeye_server_priv.key')
    app.run(host='0.0.0.0',debug=True,use_reloader=False, ssl_context=context)
    #app.run(host='0.0.0.0',debug=True,use_reloader=False)
