__author__ = 'jtorrente'

import exercise1_15 as music

def first_aid_kit():
    results = music.query_artist("First Aid Kit")
    count = 0
    for artist in results:
        if artist['name'].lower() == "first aid kit":
            count += 1
    print "NUMBER OF FIRST AID KIT BANDS = " + str(count)

def queen():
    results = music.query_artist("Queen")
    for artist in results:
        if artist['name'] == "Queen":
            #music.pretty_print(artist)
            print "BEGIN-AREA NAME FOR QUEEN = " + artist['begin-area']['name']
            break

def beatles():
    results = music.query_artist("Beatles")
    for artist in results:
        if artist['name'] == "The Beatles":
            for alias in artist['aliases']:
                if alias['locale'] == 'es':
                    print "SPANISH ALIAS NAME FOR BEATLES = " + alias['name']
            # print "BEGIN-AREA NAME FOR QUEEN = " + artist['begin-area']['name']

def nirvana():
    results = music.query_artist("Nirvana")
    for artist in results:
        if artist['name'] == "Nirvana":
            print "NIRVANA DISAMBIGUATION = "+artist['disambiguation']
            break


def one_direction():
    results = music.query_artist("One Direction")
    for artist in results:
        if artist['name'] == "One Direction":
            print "ONE DIRECTION FORMED IN = "+artist['life-span']['begin']
            break

def main():
    first_aid_kit()
    queen()
    beatles()
    nirvana()
    one_direction()

main()