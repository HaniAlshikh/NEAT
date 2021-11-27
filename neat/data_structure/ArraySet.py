import operator
import random


class ArraySet:

    def __init__(self):
        self._data = []

    def contains(self, o):
        return o in self._data

    def get_random_element(self):
        return None if len(self._data) == 0 else random.choice(self._data)

    def size(self):
        return len(self._data)

    def isempty(self):
        return not len(self._data)

    def add(self, o):
        self._data.append(o)

    def add_ordered(self, o):
        for i in range(self.size()):
            current_innovation_num = self.get(i).innovation_number
            if o.innovation_number < current_innovation_num:
                self._data.insert(i, o)
                return
        self.add(o)

    def clear(self):
        self._data.clear()

    def get(self, o):
        if not isinstance(o, (int, float, complex)):
            for e in self._data:
                if o == e:
                    return e
            return None
        return None if (o < 0 or o >= self.size()) else self._data[o]

    def get_last(self):
        return None if (self.size() == 0) else self._data[self.size() - 1]

    def remove(self, o):
        if not isinstance(o, (int, float, complex)):
            self._data.remove(o)
            return
        if not (o < 0 or o >= self.size()):
            self._data.pop(o)

    def get_data(self):
        return self._data.copy()

    # TODO: how to implement sorting in python
    def sort(self, attr):
        self._data.sort(key=operator.attrgetter(attr))

    def __iter__(self):
        return self._data.__iter__()

    def __repr__(self):
        return self._data.__repr__()
