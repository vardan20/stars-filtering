import in_out
import star
import time
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

"""all characteristics of stars, such as RA, DEC, etc."""
characteristics = []
"""number of stars in table"""
star_cnt = 0


def sort(table: dict, n: int, sort_arg: str) -> dict:
    """
    Quicksort algorithm is implemented in this function,
    It takes 3 arguments: dictionary, number of stars,
    and the characteristic by which table will be sorted.
    """
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


def run() -> None:
    """
    run method starts filtering process.
    All filtering functions are called here,
    and almost all important objects are created
    here in this file
    """

    global star_cnt
    global characteristics
    print("Data Filter process is started")
    inp = in_out.get_in()
    start_time = time.time()
    table = {}
    in_out.read_store(table, config['DEFAULT']['file_name'], inp.ra, inp.dec, inp.fov_h, inp.fov_v)

    """sort stars by magnitude"""
    table = sort(table, star_cnt, 'phot_g_mean_mag')

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
        star1 = star.Star(inp.ra, inp.dec)
        star2 = star.Star((table['ra_ep2000'][i]), (table['dec_ep2000'][i]))
        dist = star.ang_dist(star1, star2)
        table['dist'].append(dist)

    table = sort(table, star_cnt, 'dist')

    in_out.write(table, star_cnt, str(str(datetime.now())+'.csv'))

    end_time = time.time()
    print('Execution time: ', end_time-start_time, 'Sec')
