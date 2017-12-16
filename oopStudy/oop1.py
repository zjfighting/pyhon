class Dog(object):
    def __init__(self, name):
        self._name = name

    def set_name(self, value):
        self._name = value

    def get_name(self):
        return self._name

    def bark(self):
        print(self.get_name() + " is making sound wang wang")

dog = Dog("wangcai")
dog.bark()
print(dog._name)