from abc import abstractmethod, ABCMeta

class WiimoteDelegate:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_something(self):
        pass

class Delegate(WiimoteDelegate):

    def do_something(self):
        print('okay!')

delegate = Delegate()
delegate.do_something()

