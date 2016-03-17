__author__ = 'wali'

from abc import ABCMeta, abstractmethod
import numpy

class detection_system:
    __metaclass__= ABCMeta

    action_array = ['Silent','Non-Silent','Session']
    subaction_array = ['StartTab', 'CloseTab', 'StoryView', 'StoryClick', 'PageAccess', 'NotificationDropDown','MessagesDropDown',
                       'MessageBoxAccess','FriendsDropDown', 'Like', "Message", "Post", "Comment"]

    #Runtime Memory
    avg_histogram_store = dict()

    @abstractmethod
    def new_entry(self,entry,client_id,enable_detection): pass

    #Note Lazy loading will be better here
    def load_from_database(self,database):
        collections = database.collection_names()
        for collection_name in collections:
            events = database[collection_name].find()
            for event in events:
                self.new_entry(event,collection_name,False,False)

        for key in self.avg_histogram_store.keys():
            print "Client Key : " + key
            print self.avg_histogram_store.get(key)

    def alarm(self,data,email):
        print "Alarm! Send Mail"
        # SEND MAIL DAEMON HERE


########################################################################################################################
