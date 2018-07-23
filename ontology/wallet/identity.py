class Identity(object):
    def __init__(self):
        self.ontid = ""
        self.label = ""
        self.lock = False
        self.controls = []  # a list of Control()
        self.extra = ""