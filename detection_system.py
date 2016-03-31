__author__ = 'wali'
from abc import ABCMeta, abstractmethod
from pymongo import MongoClient
import unicodedata
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class detection_system:
    __metaclass__= ABCMeta

    action_array = ['Silent','Non-Silent','Session']
    subaction_array = ['StartTab', 'CloseTab', 'StoryView', 'StoryClick', 'PageAccess', 'NotificationDropDown','MessagesDropDown',
                       'MessageBoxAccess','FriendsDropDown', 'Like', "Message", "Post", "Comment"]

    #Runtime Memory
    runtime_store = dict()

    #Database_Store
    mongoClient = MongoClient()
    dataBase = mongoClient['detection-store']

    def init_database(self,collection_name):
        self.is_database_init = True
        self.collection = collection_name


    def add_to_database(self,entry):
        if(self.is_database_init):
            self.dataBase[self.collection].insert_one(entry)
        else:
            error_str = 'Failed. Database Not initialized'
            print error_str
            raise Exception(error_str)

    def update_database(self,id_key,id,entry):
        if(self.is_database_init):
            return self.dataBase[self.collection].replace_one({id_key: id},entry)
        else:
            error_str = 'Failed. Database Not initialized'
            print error_str
            raise Exception(error_str)

    def get_from_database(self, id_key, id):
        if(self.is_database_init):
            collection = self.dataBase[self.collection]
            return collection.find({id_key: id})
        else:
            error_str = 'Failed. Database Not initialized'
            print error_str
            raise Exception(error_str)

    @abstractmethod
    def new_entry(self,entry,client_id,enable_detection): pass

    #Note Lazy loading will be better here
    def load_from_database(self,database):
        collections = database.collection_names()
        for collection_name in collections:
            events = database[collection_name].find()
            for event in events:
                self.new_entry(event,collection_name,False,False)

        # for key in self.runtime_store.keys():
        #     print "Client Key : " + key
        #     print self.runtime_store.get(key)

    def alarm(self,clientid,subject,specfic_msg):

        YOUR_MAIL_SERVER = ""
        YOUR_MAIL_SERVER_PORT = 587 # default

        YOUR_EMAIL_ADDRESS = ""
        YOUR_EMAIL_LOGIN = ""
        YOUR_EMAIL_LOGIN_PASSWORD = ""


        print "Sending Mail...."
        mongomailClient = MongoClient()
        dataBase_email = mongomailClient['client_to_email']
        document = dataBase_email['emails'].find_one({"ClientID": clientid})
        if document is None:
            print "Failed to find Client's Email"
            return
        msg = MIMEMultipart()
        msg['From'] = YOUR_EMAIL_ADDRESS
        msg['To'] = document['Email']
        msg['Subject'] = '[ThirdEye] ' + subject
        final_message = 'Dear User (id : ' + clientid + ')\n'
        final_message = final_message + 'A ThirdEye notification was generated for you.\n Details:\n'
        final_message = final_message + specfic_msg
        final_message = final_message + "\n Thanks! \n ThirdEye Team"
        msg.attach(MIMEText(final_message))

        mailserver = smtplib.SMTP(YOUR_MAIL_SERVER,YOUR_MAIL_SERVER_PORT)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(YOUR_EMAIL_LOGIN, YOUR_EMAIL_LOGIN_PASSWORD)

        mailserver.sendmail(YOUR_EMAIL_ADDRESS,[document['Email']],msg.as_string())

        mailserver.quit()
        print "Sent!"


########################################################################################################################
