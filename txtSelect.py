import json


class JSONAble(object):
    def __init__(self):
        '''
        Constructor
        '''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def getValue(self, v):
        if (hasattr(v, "asJSON")):
            return v.asJSON()
        elif type(v) is dict:
            return self.reprDict(v)
        elif type(v) is list:
            vlist = []
            for vitem in v:
                vlist.append(self.getValue(vitem))
            return vlist
        else:
            return v

    def reprDict(self, srcDict):
        '''
        get my dict elements
        '''
        d = dict()
        for a, v in srcDict.items():
            d[a] = self.getValue(v)
        return d

    def asJSON(self):
        '''
        recursively return my dict elements
        '''
        return self.reprDict(self.__dict__)

me = JSONAble()
me.name = input("Введите имя\n")
me.age = int(input("Возраст\n"))



print(me.asJSON())