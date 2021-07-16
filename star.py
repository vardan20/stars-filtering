import math

class Star:

    def __init__(self, ra = 0, dec = 0):
        self.ra = float(ra)
        self.dec = float(dec)


def ang_dist(s1: Star, s2: Star):
    '''
    ang_dist() function takes coordinates of two stars,
    and returns angular distance between them
    here is the formula:
    cos(γ)=cos(90°−δa)cos(90°−δb)+sin(90°−δa)sin(90°−δb)cos(αa−αb)
    '''
    a = math.cos(math.radians(90-s1.dec))*math.cos(math.radians(90-s2.dec))
    b = math.sin(math.radians(90-s1.dec))*math.sin(math.radians(90-s2.dec))*math.cos(math.radians(s1.ra-s2.ra))
    return math.degrees(math.acos(a+b))