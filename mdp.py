__author__ = 'wali'
from detection_system import detection_system

# class TransitionMatrix:
#
#     def __init__(self):
#         self.
#         self.current_state = ''
#
#
#
#     def get_probability(self,event):
#         from_state = detection_system.subaction_array.index(self.current_state)
#         to_state = detection_system.subaction_array.index(event['ActionSubClass'])
#         prob = self.matrix[from_state][to_state] / sum(self.matrix[from_state])
#         return prob


class mdp_variant(detection_system):

    def __init__(self):
        print 'Initiating MDP variant'
        self.init_database('MDP')
        self.queue = []
        self.action_window = 10
        self.action_threshold = 5

    def new_entry(self,entry,client_id,enable_detection,printout):
        cursor = self.get_from_database('cid',client_id)

        if(cursor.count() is 1):
            #Valid Record
            Transition_Matrix_Record = cursor[0]
        elif (cursor.count() is 0):
            # No previous record
            matrix = [[0 for x in range(13)] for x in range(13)]
            Transition_Matrix_Record = {'cid': client_id, 'Matrix' : matrix,'Curr_state': 'empty'}
            self.add_to_database(Transition_Matrix_Record)
        else:
            # Cursor Error : Retruned More than one
            print "ERROR : Cursor retreived more than one Transition Matrix for a single Client id"
            return

        if (enable_detection is False):
            #Build Transition Matrix
            Transition_Matrix_Record = self.add_to_matrix(entry,Transition_Matrix_Record)
            print sum(map(sum, Transition_Matrix_Record['Matrix']))
        else:
            #Test Transition Matrix
            probability = self.get_probability(entry,Transition_Matrix_Record)
            print probability
            if(len(self.queue) == self.action_window):
                self.queue.pop()
            self.queue.insert(0,probability)
            print " Queue : " + str(self.queue)
            if (len(self.queue) == self.action_window and sum(self.queue) < self.action_threshold):
                print "Raising an Alarm"
                print "Threshhold is " + str(self.action_threshold) + " and sum of probability is " + str(sum(self.queue))


        try:
            #print Transition_Matrix_Record
            self.update_database('cid',Transition_Matrix_Record['cid'],Transition_Matrix_Record)
        except Exception as Error:
                print "Database addition Faliure" + repr(Error)



    def add_to_matrix(self,event,Transition_Matrix_Record):
        if(Transition_Matrix_Record['Curr_state'] == 'empty'):
            Transition_Matrix_Record['Curr_state'] = event['ActionSubClass'] #Should be a start tab since current state is not init
            return Transition_Matrix_Record

        from_state = detection_system.subaction_array.index(Transition_Matrix_Record['Curr_state'])
        to_state = detection_system.subaction_array.index(event['ActionSubClass'])
        Transition_Matrix_Record['Matrix'][from_state][to_state] = Transition_Matrix_Record['Matrix'][from_state][to_state] + 1
        Transition_Matrix_Record['Curr_state'] = event['ActionSubClass']
        return Transition_Matrix_Record

    def get_probability(self,event,Transition_Matrix_Record):
        print Transition_Matrix_Record
        from_state = detection_system.subaction_array.index(Transition_Matrix_Record['Curr_state'])
        to_state = detection_system.subaction_array.index(event['ActionSubClass'])
        prob = float(Transition_Matrix_Record['Matrix'][from_state][to_state]) / sum(Transition_Matrix_Record['Matrix'][from_state])
        return prob