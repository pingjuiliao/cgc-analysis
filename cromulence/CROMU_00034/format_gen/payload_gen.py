#!/usr/bin/env python
from enum import Enum, auto
from pwn import *

class Title(Enum) :
    IDENTITY = auto()
    MOVIES = auto()
    VEHICLES = auto()
    BOOKS = auto()
    SONGS = auto()
    JOBS = auto()
    HOBBIES = auto()
    PETS = auto()
    TITLE_COUNT = auto()

class Hobbies(Enum) :
    SHOOTING = auto()
    KNIVES = auto()
    STAMPS = auto()
    KAYAKING = auto()
    COINS = auto()
    EXERCISES = auto()
    SPORTS = auto()
    LAST_HOBBY = auto()




def main() :
    if len(sys.argv) <= 1 :
        off = 8
    else :
        off = int(sys.argv[1])

    buff  = header_gen(off) + ( off - 8 ) * "\x77"
    # buff += chapter_gen() + entry_gen()

    payload = whole_payload_gen(buff)

    with open("payload", "wb") as f :
        f.write(payload)
        f.close()


def whole_payload_gen(buf) :
    if len(buf) > 1234 or len(buf) < 8 :
        print "length of buffer is too much "
        quit()
    else :
        return p16(len(buf)) + buf

def header_gen(offset) :
    if offset > 0x10000 :
        print "The offset is too big ! It should be between 8 - 0x10000"
        quit()
    magic_bytes  = "BB"
    unused_bytes = "\x00\x00"
    offset_to_first_chapter = p16(offset).ljust(4, "\x00")
    return magic_bytes + unused_bytes + offset_to_first_chapter

def chapter_gen()
    title = randint(0, TITLE_COUNT)
    entry_count = randint()



if __name__ == "__main__" :
    main()
