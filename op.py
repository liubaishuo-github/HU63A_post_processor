global block_number, gl, last_pch_point, last_apt_point, feedrate
block_number = 1
gl = 9.35


import re

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
class Normal():
    i, j, k = 0.0, 0.0, 0.0
class Angle():
    b, c = 0.0, 0.0
    def b_str(self):
        return 'B' + str(round(self.b,3))
    def c_str(self):
        return 'C' + str(round(self.c,3))
    def print_angle(self):
        return self.b_str() + self.c_str()
class Apt_point():
    point = Point()
    normal = Normal()
    def extract_point_and_normal(self, apt_txt):
        temp = re.findall('-?\d+\.\d+', apt_txt)
        self.point.x, self.point.y, self.point.z, \
            self.normal.i, self.normal.j, self.normal.k= \
            list(map(float,temp))
class G_code():
    status_G90 = 0
    status_G54 = 0
    status_G0 = 0
    status_G1 = 0
    status_G43 = 0
    G90, G54, G0, G1, G43 = 'G90', 'G54', 'G0', 'G1', 'G43'

    def print_G90(self):
        if self.status_G90 == 0:
            self.status_G90 = 1
            return 'G90'
    def print_G54(self):
        pass
    def print_G0(self):
        pass
    def print_G1(self):
        pass
    def print_G43(self):
        pass

class Pch_point():
    g_code = G_code()
    point = Point()
    angle = Angle()
    feedrate = 0



def GOTO(apt_str):
    global last_apt_point, last_pch_point
    def transf(apt_point):
        from numpy import mat
        from math import sin, cos, radians, degrees, \
                        radians, asin, atan2, fabs, pi

        def translation_z(dis):
            t = mat([
                        [ 1, 0, 0, 0],
                        [ 0, 1, 0, 0],
                        [ 0, 0, 1, dis],
                        [ 0, 0, 0, 1],
                                        ])
            return t
        def translation_x(dis):
            t = mat([
                        [ 1, 0, 0, dis],
                        [ 0, 1, 0, 0],
                        [ 0, 0, 1, 0],
                        [ 0, 0, 0, 1],
                                        ])
            return t
        def rot_y(de):
            t = mat([
                        [ cos(de), 0, sin(de), 0],
                        [ 0,       1,       0, 0],
                        [-sin(de), 0, cos(de), 0],
                        [0, 0, 0, 1]
                                                    ])
            return t
        def rot_x(de):
            t = mat([
                        [1, 0, 0, 0],
                        [0, cos(de), -sin(de), 0],
                        [0, sin(de), cos(de), 0],
                        [0, 0, 0, 1]
                                                    ])
            return t
        def nearest_c(de):
            ''' de is in radians '''
            nearest_c = de
            c = radians(last_pch_point.angle.c)
            target = c - de
            if target == 0:
                return de
            if c - de > 0:
                sign = 1
            else:
                sign = -1
            delta = 2 * pi * sign
            temp = de
            while fabs(temp - c) > pi:
                temp = temp + delta
            return temp

        apt_plus_gl_point = mat([apt_point.point.x + apt_point.normal.i * gl,\
                                apt_point.point.y + apt_point.normal.j * gl,\
                                apt_point.point.z + apt_point.normal.k * gl,\
                                1]).T
        if apt_point.normal.j != 0 or apt_point.normal.k != 0:
            c_pending1 = atan2(apt_point.normal.j, apt_point.normal.k)
        else:
            c_pending1 = radians(last_pch_point.angle.c)
            print('caution,j,k = 0!')
        b_pending1 = atan2(apt_point.normal.i,
                            apt_point.normal.j * sin(c_pending1) + \
                            apt_point.normal.k * cos(c_pending1))
        c_pending2 = c_pending1 + pi
        b_pending2 = pi - b_pending1
        #print('for bug:',last_pch_point.angle.__dict__)
        #print('c_pending1=',c_pending1)
        #print('c_pending2=',c_pending2)
        if cos(c_pending1 - radians(last_pch_point.angle.c)) >= cos(c_pending2 - radians(last_pch_point.angle.c)):
            c, b = nearest_c(c_pending1), b_pending1
        else:
            c, b = nearest_c(c_pending2), b_pending2
        pch_xyz = translation_z(-37.3964) * rot_y(-b) * rot_x(c) *translation_x(3) * apt_plus_gl_point
        x, y, z = pch_xyz[0,0], pch_xyz[1,0], pch_xyz[2,0]
        return x, y, z, degrees(b), degrees(c)

    def print_pch(current_pch_point):
        pass


    current_apt_point = Apt_point()
    current_apt_point.extract_point_and_normal(apt_str)
    current_pch_point = Pch_point()


    #print(';=====')
    #print(last_pch_point.angle.c)


    current_pch_point.point.x, current_pch_point.point.y, current_pch_point.point.z\
    ,current_pch_point.angle.b,current_pch_point.angle.c = transf(current_apt_point)
    print(current_pch_point.point.__dict__)
    print(current_pch_point.angle.__dict__)
    print('========')
    last_apt_point = current_apt_point
    last_pch_point = current_pch_point
    return 1, 88



def main(apt_txt):
    #print(';=====')
    #print(last_pch_point.angle.c)
    ppword_list = ['GOTO', 'PPRINT', 'RAPID', 'FEEDOVER', 'FEDRAT', 'STOP',\
                    'SPINDLE']
    pch_txt = []

    for i in apt_txt:
        for j in ppword_list:
            ppword_match_object = re.match(j,i)
            if ppword_match_object:
                ppword = ppword_match_object.group()
                #print("match success:" + j)
                lc = locals()
                exec('temp =' + ppword + '(i)')
                temp = lc['temp']
                #print(temp)
                if temp[0] == 1:
                    pch_txt.append(temp[1])
                elif temp[0] ==2:
                    pch_txt.extend(temp[1])
                break



last_pch_point = Pch_point()
last_apt_point = Apt_point()
