import logging
import csv

characteristics = [] #all characteristics of stars, such as RA, DEC, etc.

def read(filename):
    global characteristics
    with open(filename) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        next(rd)
        characteristics = (next(rd))
        dct = {}
        for cur_char in characteristics:
            dct[cur_char] = []
        for row in rd:
            char_id = 0
            for cur_char in characteristics:
                dct[cur_char].append(row[char_id])
                char_id += 1

    return dct


class DataFilter:
    def run(self):
        print("Data Filter process is started")
        table = read("337.all.tsv")
        #print(table['ra_ep2000'][0:5])
        #print(characteristics)
