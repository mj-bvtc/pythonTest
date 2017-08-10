import uuid
import LogStamp



class Common(object):
    def __init__(self):
        self.id = uuid.uuid4()
        self.user = LogStamp.get_user()
        self.dt = LogStamp.get_datetime()
        self.mac = LogStamp.get_machine()
