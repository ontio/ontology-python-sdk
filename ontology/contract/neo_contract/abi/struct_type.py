class Struct(object):
    def __init__(self, struct: list):
        self.param_list = struct

    def add(self, *objs):
        for obj in objs:
            self.param_list.append(obj)

