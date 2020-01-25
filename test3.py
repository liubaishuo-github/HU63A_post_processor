global aaaa


aaaa = 33
def c():
    print('sdfjsldfj')

def a():
    #print('it\'s in a, aaaa=', aaaa)
    def b():
        global aaaa
        print('it\'s in b, aaaa=', aaaa, sep='')
        aaaa = 999
        c()
    b()
    print('it\'s in a, aaaa=', aaaa, sep='')




a()
