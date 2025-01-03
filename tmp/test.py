def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        print(func())
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    return "hellooooo"

say_hello()