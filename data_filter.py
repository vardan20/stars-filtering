import logging
import csv
import get_input
import star


characteristics = [] #all characteristics of stars, such as RA, DEC, etc.
star_cnt = 0 #number of stars in table


def filter_by_fov(table, ra: float, dec: float, fov_h: float, fov_v: float):
    '''
    The filter_by_fov function filters the table of stars
    and keeps the stars which are located in given FOV
    '''
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


def sort(table,n,sort_arg):
    '''
    Quicksort algorithm is implemented in this function,
    It takes 3 arguments: dictionary, number of stars,
    and the characteristic by which table will be sorted.
    '''
    if n<=1:
        return table
    pivot = table[sort_arg][n//2]
    left, middle, right, ans = {},{},{},{}
    for i in characteristics:
        left[i], middle[i], right[i], ans[i] = [], [], [], []
    for id in range(n):
        x = table[sort_arg][id]
        if x<pivot:
            for i in characteristics:
                left[i].append(table[i][id])
        elif x == pivot:
            for i in characteristics:
                middle[i].append(table[i][id])
        else:
            for i in characteristics:
                right[i].append(table[i][id])

    left = sort(left, len(left[sort_arg]), sort_arg)
    right = sort(right, len(right[sort_arg]), sort_arg)
    for i in characteristics:
        ans[i] = left[i]+middle[i]+right[i]
    return ans


class DataFilter:
    def run(self):
        global star_cnt
        print("Data Filter process is started")
        # s1 = star.Star(101.28,-16.71)
        # s2 = star.Star(24.43, -57.2)
        # print(star.ang_dist(s1,s2))
        inp = get_input.GetInput()
        inp.input()
        table = inp.read_store('337.all.tsv')
        table = filter_by_fov(table, float(inp.ra), float(inp.dec), float(inp.fov_h), float(inp.fov_v))
        #print("After FOV filtering {} stars are left".format(star_cnt))

        table = sort(table,star_cnt,'phot_g_mean_mag')

        # This statement checks if we have more than N stars left,
        # if we do, we need to take the brightest N ones
        if inp.N<star_cnt:
            star_cnt = inp.N
            for it in characteristics:
                table[it] = table[it][0:star_cnt]

        for i in range(star_cnt):
              print(table['ra_ep2000'][i],table['phot_g_mean_mag'][i])