__author__ = 'wali'
from detection_system import detection_system
import numpy

class Histogram:
    def __init__(self):
        self.table = dict()
        self.events = 0

    def add_event(self,event):
        action_class = event['ActionClass']
        action_subclass = event['ActionSubClass']

        if(not self.table.has_key(action_class)):
            self.table[action_class] = 0

        if(not self.table.has_key(action_subclass)):
            self.table[action_subclass] = 0

        current_value = self.table.get(action_class)
        self.table[action_class] = current_value + 1

        current_value = self.table.get(action_subclass)
        self.table[action_subclass] = current_value + 1

        self.events = self.events + 1

    def __str__(self):
        print "------- HISTOGRAM --------"
        print "Events : " + str(self.events)
        for key, value in self.table.iteritems() :
            print key, value
        print "-------    End    --------"
        return ""

class Avg_Histogram:

    def __init__(self):
        self.list_containing_table = dict()
        for action in detection_system.action_array:
            self.list_containing_table[action] = list()
        for subaction in detection_system.subaction_array:
            self.list_containing_table[subaction] = list()

    def add_histogram(self, curr_histogram):
        present_keys = curr_histogram.table.keys()
        total_keys = detection_system.subaction_array + detection_system.action_array
        absent_keys = list(set(total_keys) - set(present_keys))

        for key in present_keys:
            key_list = self.list_containing_table.get(key)
            key_list.append(curr_histogram.table.get(key))

        for key in absent_keys:
            key_list = self.list_containing_table.get(key)
            key_list.append(0)

    def __str__(self):
        print "----- AVG HISTOGRAM -----"
        mean_values = dict()
        stddev_values = dict()
        all_keys = self.list_containing_table.keys()
        for key in all_keys:
            mean_values[key] = numpy.mean(self.list_containing_table[key])
            stddev_values[key] = numpy.std(self.list_containing_table[key])
        for key in all_keys:
            print str(key) + " Mean : " + str(mean_values.get(key)), " Std : " + str(stddev_values.get(key))
        print "----- END -----"
        return ""

class histo_detection(detection_system):

    def __init__(self):
        self.current_histogram = Histogram()
        self.action_window = 15

    def new_entry(self,entry,client_key,enable_detection,print_out):
        if( not self.runtime_store.has_key(client_key)):
            self.runtime_store[client_key]= Avg_Histogram()

        if(self.current_histogram.events < self.action_window):
            self.current_histogram.add_event(entry)

        if(self.current_histogram.events == self.action_window):
            result = False #Default State
            if(print_out) : print self.current_histogram

            #If detection is enabled, check if current historgram is too far from average
            if(enable_detection):
                result = self.detect(client_key)

            # No Alarm was raised
            if(result is False):
                avg_histogram = self.runtime_store.get(client_key)
                avg_histogram.add_histogram(self.current_histogram)
                self.runtime_store[client_key] = avg_histogram
            # An Alarm was raised
            else:
                self.alarm(self.current_histogram,client_key)

            #Reset Current Histogram
            self.current_histogram = Histogram()

    def detect(self, client_key):
        print "detecting"
        avg_histogram = self.runtime_store.get(client_key)
        mean_values = dict()
        stddev_values = dict()
        all_keys = avg_histogram.list_containing_table.keys()
        for key in all_keys:
            mean_values[key] = numpy.mean(avg_histogram.list_containing_table[key])
            stddev_values[key] = numpy.std(avg_histogram.list_containing_table[key])
            # Adding 0 Value in current histogram if this key is missing
            if(not self.current_histogram.table.has_key(key)):
                self.current_histogram.table[key] = 0

        key_to_check = ['Silent','Non-Silent']
        for key in key_to_check:
            abs_diff_current_and_mean = abs(self.current_histogram.table.get(key) -mean_values.get(key))
            if abs_diff_current_and_mean > (2*stddev_values.get(key)) or abs_diff_current_and_mean < (2*stddev_values.get(key)):
                print "-----  FLAGGING ANOMALY -----"
                print "Action :" + str(key)
                print "Observed Value : " + str(self.current_histogram.table.get(key)) + " Mean Value : " + str(mean_values.get(key)) + " Std Dev : " + str(stddev_values.get(key))
                print "-----         END       ----- "


        return False