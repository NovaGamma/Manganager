from io import StringIO
import sys
import time

def logdecorator(func):
    def inner(*args, **kwargs):
        logger = Logger()
        recursive = False
        if sys.stdout != sys.__stdout__:
            recursive = True
        else:
            sys.stdout = logger
            sys.stderr = logger
        func(*args, **kwargs)
        if not recursive:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
    return inner

def log(class_):
    for attr in class_.__dict__:
        if callable(getattr(class_, attr)):
            setattr(class_, attr, logdecorator(getattr(class_, attr)))
    return class_

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(StringIO, metaclass=Singleton):
    def __init__(self):
        t = time.strftime("%a_%b_%d_%H_%M_%S_%Y")
        t = t.replace(" ", "_").replace(":","_")
        self.time = t
        self.previous = ''

    def write(self, *args):
        try:
            with open(f"logs/{self.time}.txt", 'a') as file:
                if not self.previous or '\n' in self.previous:
                    file.write(f"[{time.strftime('%a %b %d %H:%M:%S %Y')}]: {args[0]}")
                else:
                    file.write(f"{args[0]}")
            sys.__stdout__.write(*args)
            self.previous = args[0]
        except Exception as err:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            raise err