import sys

def modelbuilder():
    print('test started')


class Fra(object):
    def initialize(self, **kwargs):
        for item in kwargs.items:
            key_, value_ = item
            if self._property_.key == key_:
                self._property_[key_] = value_

    def __init__(self, **kwargs):
        self._property_ = {}
        if ['_target', '_ccy', '_start', '_end'] not in kwargs.keys():
            print('err: not enough to build obj')
            pass
        else:
            self.initialize(self, kwargs)

    def get_target(self):
        return self._property_['_target']

    def get_penalty(self):
        if [] not in self._property_.keys():
            pass

    def get_annuity(self):
        return 0






if __name__ == '__main__':
    print('test end')
    modelbuilder()
    print('test end')
else:
    print('not run')

print(__name__)