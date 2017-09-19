class Vector2d:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))


def main():
    vector2d = Vector2d(1, 2)


if __name__ == '__main__':
    main()
