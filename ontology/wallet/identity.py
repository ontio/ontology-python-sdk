did_ont = "did:ont:"


class Identity(object):
    def __init__(self, ontid="", label="", lock=False, controls=[]):
        self.ontid = ontid
        self.label = label
        self.lock = lock
        self.controls = controls  # a list of Control()



