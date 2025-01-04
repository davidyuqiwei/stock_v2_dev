# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         print(func())
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_hello():
#     return "hellooooo"

# say_hello()


class Animal:
    def __init__(self):
        self.name = "animal"

    def speak(self):
        return f"{self.name} makes a sound."


class Dog(Animal):
    def __init__(self):
        #super().__init__()  # 调用父类的构造函数
        self.name = "ttt"

    def speak(self):
        return super().speak() + " Woof!"  # 扩展父类的方法

dog = Dog()
print(dog.speak())  # 输出: Buddy makes a sound. Woof!