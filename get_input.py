import csv
import data_filter

class GetInput:
    '''
    GetInput class organizes user input,
    input() and show() methods are implemented,
    which read and print user data
    '''
    # def __init__(self, ra, dec, fov_h,fov_v, N):
    #     self.ra = ra
    #     self.dec = dec
    #     self.fov_h = fov_h
    #     self.fov_v = fov_v
    #     self.N = N
    def input(self):
        self.ra, self.dec  = input("Please Enter equatorial coordinates (ra, dec): ").split()
        self.fov_h, self.fov_v = input("Please Enter horizontal and vertical FOV: ").split()
        self.N = int(input("Please Enter the number of Stars N: "))


    def show(self):
        print(self.ra, self.dec, self.fov_h, self.fov_v, self.N, end = ' ')


    def read_store(self,filename):

        '''
        The read_store() function takes a filename as a parameter,
        and stores the information of that file in a
        dictionary, and returns it.
        '''

        with open(filename) as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            next(rd)
            data_filter.characteristics = (next(rd))
            data_filter.characteristics.append('id')
            dct = {}
            for cur_char in data_filter.characteristics:
                dct[cur_char] = []
            for row in rd:
                dct['id'].append(data_filter.star_cnt)
                char_id = 0
                data_filter.star_cnt += 1
                for cur_char in data_filter.characteristics:
                    if cur_char == 'id':
                        continue
                    dct[cur_char].append(row[char_id])
                    char_id += 1

        return dct


    def write(self, table, n, filename):
        f = open(filename,'w')
        writer = csv.writer(f)
        row = ['id','source_id', 'ra_ep2000', 'dec_ep2000', 'phot_g_mean_mag', 'angular_distance']
        writer.writerow(row)
        for i in range(n):
            row = [table['id'][i],table['source_id'][i], table['ra_ep2000'][i], table['dec_ep2000'][i],
                   table['phot_g_mean_mag'][i], table['dist'][i]]
            writer.writerow(row)
        f.close()