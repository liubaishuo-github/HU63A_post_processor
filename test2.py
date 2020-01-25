class Point():
    x , y, z = 0, 0, 0
    def x_str(self):
        return 'X' + str(round(self.x,4))
    def y_str(self):
        return 'Y' + str(round(self.y,4))
    def z_str(self):
        return 'Z' + str(round(self.z,4))
    def print_point(self):
        return self.x_str() + self.y_str() + self.z_str()



point = Point()
if point.x == 0:
    print('ok')
