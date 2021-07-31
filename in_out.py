import csv
import data_filter


'''
GetInput module organizes user input,
input(), show(), read_store() and write()
methods are implemented, which read and print user data,
store data in dictionary, and writes final form
in a new csv file
'''


class InputData:
    def __init__(self, ra, dec, fov_h, fov_v, n):
        self.ra = ra
        self.dec = dec
        self.fov_h = fov_h
        self.fov_v = fov_v
        self.n = n


def get_in() -> InputData:
    # takes all required input from user
    ra, dec = input("Please Enter equatorial coordinates (ra, dec): ").split()
    fov_h, fov_v = input("Please Enter horizontal and vertical FOV: ").split()
    n = int(input("Please Enter the number of Stars N: "))
    return InputData(ra, dec, fov_h, fov_v, n)


def read_store(dct, filename):
    """
    The read_store() method takes a filename as a parameter,
    and stores the information of that file in a
    dictionary.
    """

    with open(filename) as fd:
        id_n = 0
        for i in fd:
            item = i.split('\t')
            if id_n == 0:
                id_n += 1
                continue

            if id_n == 1:
                data_filter.characteristics.append('id')
                data_filter.characteristics.append('ra_ep2000')
                data_filter.characteristics.append('dec_ep2000')
                data_filter.characteristics.append('source_id')
                data_filter.characteristics.append('phot_g_mean_mag')

                for cur_char in data_filter.characteristics:
                    dct[cur_char] = []
            else:
                dct['id'].append(data_filter.star_cnt)
                data_filter.star_cnt += 1
                dct['ra_ep2000'].append(item[0])
                dct['dec_ep2000'].append(item[1])
                dct['source_id'].append(item[7])
                dct['phot_g_mean_mag'].append(item[22])
            id_n += 1


def write(table, table_0, n, filename):
    """
    write method take data from the filtered table and
    writes it in filename.csv file
    """

    f = open(filename, 'w')
    writer = csv.writer(f)
    row = ['id', 'source_id', 'ra_ep2000', 'dec_ep2000', 'phot_g_mean_mag', 'angular_distance']
    writer.writerow(row)
    table['source_id'] = []
    for i in range(n):
        row = [table['id'][i], table_0['source_id'][table['id'][i]],
               table_0['ra_ep2000'][table['id'][i]], table_0['dec_ep2000'][table['id'][i]],
               table['phot_g_mean_mag'][i], table['dist'][i]]
        writer.writerow(row)
    f.close()
