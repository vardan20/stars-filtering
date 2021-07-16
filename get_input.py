import csv
import data_filter


class GetInput:
    '''
    GetInput class organizes user input,
    input(), show(), read_store() and write()
    methods are implemented, which read and print user data,
    store data in dictionary, and writes final form
    in a new csv file
    '''

    def input(self):
        # takes all requried input from user
        self.ra, self.dec  = input("Please Enter equatorial coordinates (ra, dec): ").split()
        self.fov_h, self.fov_v = input("Please Enter horizontal and vertical FOV: ").split()
        self.N = int(input("Please Enter the number of Stars N: "))


    def show(self):
        # prints user input data
        print(self.ra, self.dec, self.fov_h, self.fov_v, self.N, end = ' ')


    def read_store(self,filename):
        '''
        The read_store() method takes a filename as a parameter,
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


    def write(self, table,table_0, n, filename):
        '''
        write method take data from the filtered table and
        writes it in filename.csv file
        '''
        f = open(filename,'w')
        writer = csv.writer(f)
        row = ['id','source_id','ra_ep2000', 'dec_ep2000','phot_g_mean_mag','angular_distance']
        writer.writerow(row)
        table['source_id'] = []
        for i in range(n):
            row = [table['id'][i],table_0['source_id'][table['id'][i]],
                   table_0['ra_ep2000'][table['id'][i]], table_0['dec_ep2000'][table['id'][i]],
                   table['phot_g_mean_mag'][i], table['dist'][i]]
            writer.writerow(row)
        f.close()