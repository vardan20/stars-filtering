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
        self.N = input("Please Enter the number of Stars N: ")


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
            dct = {}
            for cur_char in data_filter.characteristics:
                dct[cur_char] = []
            for row in rd:
                char_id = 0
                data_filter.star_cnt += 1
                for cur_char in data_filter.characteristics:
                    dct[cur_char].append(row[char_id])
                    char_id += 1

        return dct