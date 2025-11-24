class Jar:
    def __init__(self, capacity=12, size=0):
        self._capacity = capacity
        self._size = size

    def __str__(self):
        return self.size * "🍪"

    def deposit(self, n):
        if self._capacity > self._size + n:
            self._size = self._size + n
        else:
            raise ValueError

    def withdraw(self, n):
        if 0 <= self._size - n:
            self._size = self._size - n
        else:
            raise ValueError

    @property
    def capacity(self):
        if self._capacity >= 0:
            return self._capacity
        else:
            raise ValueError
    @property
    def size(self):
        return self._size