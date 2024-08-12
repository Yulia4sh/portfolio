class Vector:
    def __init__(self, x, y, z=None):
        if isinstance(x, Vector):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = x
            self.y = y
            self.z = z

    @property
    def coordinates(self):
        if self.z is None:
            return self.x, self.y
        return self.x, self.y, self.z

    def __str__(self):
        return f"Vector({self.coordinates})"

    def __add__(self, other):
        if self.z is None:
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if self.z is None:
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + (self.z * other.z if self.z and other.z else 0)

    def cross(self, other):
        if self.z is None or other.z is None:
            raise ValueError("Векторний добуток можна обчислювати лише для 3D векторів")
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def __eq__(self, other):
        if self.z is None and other.z is None:
            return self.x == other.x and self.y == other.y
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            if self.z is not None:
                return self.z
            else:
                raise IndexError("Index out of range for 2D vector")
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            if self.z is not None:
                self.z = value
            else:
                raise IndexError("Index out of range for 2D vector")
        else:
            raise IndexError("Index out of range")