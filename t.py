# decorator testing

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something pre")
        func(*args, **kwargs)
        print("Something post")

    return wrapper


@my_decorator
def testing(num: int):
    print(num)


testing(3)
