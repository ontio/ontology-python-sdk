class Struct(object):
    def __init__(self):
        self.param_list = []

    def add(self, *objs):
        for obj in objs:
            self.param_list.append(obj)