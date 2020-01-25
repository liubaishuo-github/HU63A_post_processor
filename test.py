import re

apt = "-8.249664, -16.502253,   8.441231,\
        -0.515603993,-0.675140814,0.527576917"



class Point():
    x ,y, z = 0, 0, 0
class Normal():
    i, j, k = 0, 0, 0
class apt_point():

    point = Point()
    normal = Normal()
    def extract_point_and_normal(self, apt_txt):
        temp = re.findall('-?\d+\.\d+', apt_txt)
        self.point.x, self.point.y, self.point.z, \
            self.normal.i, self.normal.j, self.normal.k= \
            list(map(float,temp))


apt_point = apt_point()
apt_point.extract_point_and_normal(apt)

print(apt_point.point.__dict__)
print(apt_point.normal.__dict__)
