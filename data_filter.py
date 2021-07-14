import logging
import csv
import get_input

characteristics = [] #all characteristics of stars, such as RA, DEC, etc.
star_cnt = 0 #number of stars in table
def read(filename):
    global characteristics
    global star_cnt
    with open(filename) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        next(rd)
        characteristics = (next(rd))
        dct = {}
        for cur_char in characteristics:
            dct[cur_char] = []
        for row in rd:
            char_id = 0
            star_cnt+=1
            for cur_char in characteristics:
                dct[cur_char].append(row[char_id])
                char_id += 1

    return dct


def filter_by_fov(table, ra: float, dec: float, fov_h: float, fov_v: float):
    global star_cnt
    table_modifed = {}
    star_cnt_new = 0
    for x in characteristics:
        table_modifed[x] = []
    for i in range(star_cnt):
        # d1 is the RA distance between the given coordinate and i-th star
        d1 = abs(float(table['ra_ep2000'][i])-ra)
        if d1>180:
            d1 = 360-d1

        # d2 is the DEC distance between the given coordinate and i-th star
        d2 = abs(float(table['dec_ep2000'][i])-dec)

        # this two if-statements check if i-th star is in FOV or not
        if d1>fov_h/2:
            continue
        if d2>fov_v/2:
            continue
        star_cnt_new+=1
        for x in characteristics:
            table_modifed[x].append(table[x][i])
    star_cnt = star_cnt_new
    return table_modifed
class DataFilter:
    def run(self):
        print("Data Filter process is started")
        table = read("337.all.tsv")
        inp = get_input.GetInput()
        inp.input()
        table = filter_by_fov(table, float(inp.ra), float(inp.dec), float(inp.fov_h), float(inp.fov_v))
        print("After FOV filtering {} stars are left".format(star_cnt))
