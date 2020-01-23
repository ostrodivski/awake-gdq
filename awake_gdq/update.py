#!/usr/bin/python3

import time
import os

from awake_gdq.path import *
from awake_gdq.schedule import *
from awake_gdq.retriever import *


def search(sc, entry) :
    for e in iter(sc) :
        if e.compare(entry) :
            return e
    return None

## the algorithm starts from the first entries of both schedule (former and new),
## then go down step by step ; if the comparison failed, it tries to guess if it was
## an addition, deletion, permutation or substitution

def update(sc1, sc2) :
    entry1 = sc1
    entry2 = sc2
    l1 = None   # when an occurence of 2 is found in 1, this variable is set to this occurence
    l2 = None   # when an occurence of 1 is found in 2, this variable is set to this occurence
    while entry1 != None and entry2 != None :
        if entry1.marking :
            entry1 = entry1.next_sc
        if entry2.marking :
            entry2 = entry2.next_sc

        if compare(entry1, entry2) :
            # nothing to do
            entry1.copy(entry2)
            entry1 = entry1.next_sc
            entry2 = entry2.next_sc
        else :
            l1 = search(entry1, entry2)
            l2 = search(entry2, entry1)
            if compare(entry1.next_sc, entry2.next_sc) :
                if l1 == None :
                    if l2 == None :
                        # substitution
                        entry1, entry2 = substitution(sc1, entry1, entry2, l1, l2)
                    else :
                        # addition
                        entry1, entry2 = addition(sc1, entry1, entry2, l1, l2)
                else :
                    if l2 == None :
                        # deletion
                        entry1, entry2 = deletion(sc1, entry1, entry2, l1, l2)
                    else :
                        # shift :
                        entry1, entry2 = top_shift(sc1, entry1, entry2, l1, l2)
            else :
                if l1 == None :
                    # addition
                    entry1, entry2 = addition(sc1, entry1, entry2, l1, l2)
                else :
                    if l2 == None :
                        # deletion
                        entry1, entry2 = deletion(sc1, entry1, entry2, l1, l2)
                    else :
                        if compare(entry1, entry2.next_sc) :
                            # top shift
                            entry1, entry2 = top_shift(sc1, entry1, entry2, l1, l2)
                        elif compare(entry2, entry1.next_sc) :
                            # bottom shift
                            entry1, entry2 = bottom_shift(sc1, entry1, entry2, l1, l2)
                        else :
                            # filthy permutation ???
                            entry1, entry2 = top_shift(sc1, entry1, entry2, l1, l2)

    for entry in sc2 :  # don't forget to unmark the new schedule
        entry.marking = False



def deletion(sc, entry1, entry2, l1, l2) :
    log('* ' + entry1.title + ' was removed')
    return entry1.next_sc, entry2

def addition(sc, entry1, entry2, l1, l2) :
    log('* ' + entry2.title + ' was added at ' + entry2.start_date.ctime())
    identify(sc, entry2)   # don't forget to identify the new entry
    return entry1, entry2.next_sc

# the entry in 1 has been delayed
def top_shift(sc, entry1, entry2, l1, l2) :
    log('* ' + entry2.title + ' was rescheduled to ' + entry2.start_date.ctime())
    copy(l1, entry2)
    l1.marking = True
    return entry1, entry2.next_sc

# the entry in 1 has been advanced : it is the same thing as saying that
# the entry in 2 has been delayed
def bottom_shift(sc, entry1, entry2, l1, l2) :
    log('* ' + l2.title + ' was rescheduled to ' + l2.start_date.ctime())
    copy(entry1, l2)
    l2.marking = True
    return entry1.next_sc, entry2

def substitution(sc, entry1, entry2, l1, l2) :
    log('* ' + entry1.title + ' was changed to ' + entry2.title)
    copy(entry1, entry2)
    return entry1.next_sc, entry2.next_sc


def log(str) :
    log_file = os.open(os.path.join(LOCAL_PATH, 'log.txt'), os.O_WRONLY|os.O_APPEND|os.O_CREAT)
    os.write(log_file, bytes(str + '\n', 'utf-8'))
    os.close(log_file)
