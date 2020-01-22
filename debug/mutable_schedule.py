#/usr/bin/python3

from awake_gdq.schedule import *


class MutableSchedule(Schedule) :

    def __init__(self) :
        Schedule.__init__(self)

    # rewritten methods

    def new_sc(self) :
        new = MutableSchedule()
        return new

    # change methods

    def find_entry(self, entry_id) :
        for entry in iter(self) :
            if entry_id == entry.identifier :
                return entry

    def remove(self) :
        self.prev_sc.next_sc = self.next_sc
        self.next_sc.prev_sc = self.prev_sc

        self.next_sc.offset(-self.duration)

    def add(self, entry, new = True) :      # entry is added before self
                                            # if the entry is not yet in the schedule, set new to True
        self.prev_sc.next_sc = entry
        entry.prev_sc = self.prev_sc
        entry.prev_sc.next_sc = entry
        entry.next_sc = self
        self.prev_sc = entry

        if new :
            entry.is_empty = False
            entry.is_last = False
        entry.start_date = self.start_date

        self.offset(entry.duration)

    def shift(self, entry) :    # self is shifted before entry
        self.remove()
        entry.add(self, False)

    def swap(self, entry) :     # swap self and entry
        if entry == self.next_sc :
            entry.shift(self)
        else :
            next_entry = self.next_sc
            self.shift(entry)       # self is shifted before entry
            entry.shift(next_entry) # then entry is shifted before the entry that was following self
        
    def change_title(self, title) :
        self.title = title

    def offset(self, duration) : # offset from self to until by duration
        entry = self
        while not entry.is_last :
            entry.start_date = entry.start_date + duration
            entry = entry.next_sc



def remove_(entry) :
    entry.remove()

def add_(src, dst) :
    dst.add(src)

def shift_(src, dst) :
    src.shift(dst)

def swap_(entry_1, entry_2) :
    entry_1.swap(entry_2)

def change_title_(entry, title) :
    entry.change_title(title)




def find_entry(sc, entry_id) :
    return sc.find_entry(entry_id)


def remove(sc, entry_id) :
    entry = find_entry(sc, entry_id)
    remove_(entry)

def add(sc, entry_id, title, duration) :
    entry = find_entry(sc, entry_id)
    new_entry = MutableSchedule()
    new_entry.title = title
    new_entry.duration = duration
    add_(new_entry, entry)

def shift(sc, id_src, id_dst) :
    src = find_entry(sc, id_src)
    dst = find_entry(sc, id_dst)
    shift_(src, dst)

def swap(sc, id_1, id_2) :
    entry_1 = find_entry(sc, id_1)
    entry_2 = find_entry(sc, id_2)
    swap_(entry_1, entry_2)

def change_title(sc, title, entry_id) :
    entry = find_entry(sc, entry_id)
    change_title_(entry, title)
