
########################################################################################################################

# States
BASE_LINE_FOLLOWER = 0
WHITE_LINE_FOLLOWER = 1
OBJECT_AVOIDANCE = 2


########################################################################################################################


class Event(object):

    def __init__(self):
        self.eventHandlers = []

    def __iadd__(self, handler):
        self.eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.eventHandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.eventHandlers:
            eventhandler(*args, **keywargs)


########################################################################################################################


class StateController(object):

    def __init__(self):
        self.state = BASE_LINE_FOLLOWER

    def objectDetected(self):
        print("Object in sight, setting avoidance course")
        # call method to modify direction


########################################################################################################################
