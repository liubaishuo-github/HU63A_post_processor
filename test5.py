import copy
#global point2

num = 1


def a():
    num = 3
    def b():
        num = 5
        def c():
            global num
            print('c',num)
            num = 10
            print('c',num)
        print('b,before c',num)
        c()
        print('b,after c',num)
    print('a,before b',num)
    b()
    print('a,after b',num)


print('main, before a',num)


a()
print('main, after a',num)
