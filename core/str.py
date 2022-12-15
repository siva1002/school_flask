from functools import wraps
def decarator(fun):
    @wraps(fun)
    def wrap_func():
        print("************")
        fun()
    return wrap_func

@decarator
def prints():
    print('hello')
prints()