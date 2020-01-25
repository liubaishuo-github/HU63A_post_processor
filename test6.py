from math import radians, degrees, fabs, pi


def nearest_c(de):
    ''' de is in radians '''
    nearest_c = de
    c = radians(-179)
    target = c - de
    if target == 0:
        return degrees(de)
    if c - de > 0:
        sign = 1
    else:
        sign = -1
    delta = 2 * pi * sign
    temp = de
    #print(temp)
    #print(c)
    #print(delta)
    while fabs(temp - c) > pi:
        temp = temp + delta
    return degrees(temp)


print(nearest_c(radians(-179)))
