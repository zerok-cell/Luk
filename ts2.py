
class X:

    def __del__(self):
        print('x')



q = X()

q = None