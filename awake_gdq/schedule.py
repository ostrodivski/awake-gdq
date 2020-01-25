#!/usr/bin/python3


## the class schedule consists of a basic structure of chained list
##    [entry_1] <-> [entry_2] <-> ... <-> [_]
## the last entry is always empty
## there's no implementation of addition, deletion or substitution because we don't need them

class Schedule :
    def __init__(self, identified = True) :

        # id info

        # if identified is False, the programm don't assign a new identifier to each entry ;
        # the entries will get their identifier when updating, via the methods copy and identify
        self.identified = identified
        self.identifier = 0

        # structure info

        self.is_first = True
        self.is_last = True
        self.next_sc = None
        self.prev_sc = None
        self.current_sc = None  # iteration variable

        # time info

        self.time_origin = 0
        self.start_date = 0
        self.duration = 1800    # 30 minutes

        # misc info

        self.title = ''
        self.category = ''
        self.estimate = ''
        self.runners = ''

        # other

        self.marking = False     # set to True when a substitution is found


    # iteration

    def __iter__(self) :
        self.current_sc = self
        return self

    def __next__(self) :
        if self.current_sc.is_last :
            raise StopIteration
        next_sc = self.current_sc
        self.current_sc = self.current_sc.next_sc
        return next_sc

    # methods

    def initialize(self) :
        if not self.is_last :
            for entry in iter(self.next_sc) :
                del entry
        self.is_last = True
        self.identified = True

    def add_sc(self, **kwargs) :
        if not self.is_last :
            self.next_sc.add_sc(**kwargs)
        else :
            self.start_date = kwargs.get('date', 0)
            self.title = kwargs.get('title', 'Title')
            self.category = kwargs.get('category', 'Category')
            self.estimate = kwargs.get('estimate', '0:00:00')
            self.runners = kwargs.get('runners', 'Runners')

            self.is_last = False
            if self.identified and not self.is_first :
                self.identifier = self.prev_sc.identifier + 1

            self.next_sc = self.new_sc()
            self.next_sc.identified = self.identified
            self.next_sc.prev_sc = self
            self.next_sc.is_first = False

            if self.prev_sc :
                self.prev_sc.duration = self.start_date - self.prev_sc.start_date

            if self.is_first :
                self.time_origin = self.start_date
            self.next_sc.time_origin = self.time_origin

    def new_sc(self) :  # returns an object of the current class : if a class inherits from schedule,
                        # don't forget to rewrite this method
        new = Schedule()
        return new

    def identify(self, identifier) :
        self.identifier = identifier

    def compare(self, target) :
        return self.title == target.title

    def copy(self, target) :
        target.identifier = self.identifier
        target.identified = self.identified


def identify(sc, entry) :   # the chosen identifier is always greater than the others
    identifier = 0
    for e in sc :
        if identifier <= e.identifier : identifier = e.identifier + 1
    entry.identify(identifier)

def compare(entry_1, entry_2) :
    return entry_1.compare(entry_2)

def copy(src, dst) :
    src.copy(dst)
