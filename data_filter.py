import in_out
import star
import time
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


characteristics = []  #all characteristics of stars, such as RA, DEC, etc.
star_cnt = 0  #number of stars in table


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
        if d1 > fov_h/2:
            continue
        if d2 > fov_v/2:
            continue
        star_cnt_new += 1

        for x in characteristics:
            table_modifed[x].append(table[x][i])

    star_cnt = star_cnt_new
    return table_modifed


def sort(table, n, sort_arg):
    '''
    Quicksort algorithm is implemented in this function,
    It takes 3 arguments: dictionary, number of stars,
    and the characteristic by which table will be sorted.
    '''
    if n <= 1:
        return table
    pivot = table[sort_arg][n//2]
    left = {}
    middle = {}
    right = {}
    ans = {}
    for i in characteristics:
        left[i] = []
        middle[i] = []
        right[i] = []
        ans[i] = []
    for k in range(n):
        x = table[sort_arg][k]
        if x < pivot:
            for i in characteristics:
                left[i].append(table[i][k])
        elif x == pivot:
            for i in characteristics:
                middle[i].append(table[i][k])
        else:
            for i in characteristics:
                right[i].append(table[i][k])

    left = sort(left, len(left[sort_arg]), sort_arg)
    right = sort(right, len(right[sort_arg]), sort_arg)
    for i in characteristics:
        ans[i] = left[i]+middle[i]+right[i]
    return ans


class DataFilter:
    def run(self):
        '''
        run method starts filtering process.
        All filtering functions are called here,
        and almost all important objects are created
        here in this file
        '''
        global star_cnt
        global characteristics
        print("Data Filter process is started")
        inp = in_out.get_in()
        start_time = time.time()
        table = in_out.read_store(config['DEFAULT']['file_name'])
        table_0 = table
        characteristics = ['id', 'phot_g_mean_mag']

        # filter by FOV
        table = filter_by_fov(table, float(inp.ra), float(inp.dec), float(inp.fov_h), float(inp.fov_v))

        table = sort(table, star_cnt, 'phot_g_mean_mag') # sort stars by magnitude

        '''
        This statement checks if we have more than N stars left,
        if we do, we need to take the brightest N ones
        '''
        if inp.n < star_cnt:
            star_cnt = inp.n
            for it in characteristics:
                table[it] = table[it][0:star_cnt]

        '''
        This part of code adds new characteristic to our table:
        'dist' which shows the distance between given point in input
        and the particular star
        '''
        table['dist'] = []
        characteristics.append('dist')
        for i in range(star_cnt):
            table['dist'].append(star.ang_dist(star.Star(inp.ra, inp.dec),
                                 star.Star(float(table_0['ra_ep2000'][table['id'][i]]),
                                           float(table_0['dec_ep2000'][table['id'][i]]))))

        table = sort(table, star_cnt, 'dist')

        in_out.write(table, table_0, star_cnt, str(str(datetime.now())+'.csv'))

        end_time = time.time()
        print('Execution time: ', end_time-start_time, 'Sec')
