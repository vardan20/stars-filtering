
class GetInput:
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