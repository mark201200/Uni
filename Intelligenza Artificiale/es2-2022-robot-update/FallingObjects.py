class FallingObject:

    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    def __str__(self) -> str:
        s = "Object type: " + self.type + " | ( x=" + str(self.x) + ", y=" + str(self.y) + " )"
        return s


class Rock(FallingObject):

    def __init__(self, x, y, dmg):
        super().__init__("rock", x, y)
        self.dmg = dmg
        if dmg >= 3:
            self.vel = 2
        else:
            self.vel = 1

    def __str__(self) -> str:
        return super().__str__() + " | Rock damage =" + str(self.dmg) + " | Falling speed =" + str(self.vel)


class Energy(FallingObject):

        def __init__(self, x, y):
            super().__init__("energy", x, y)
            self.vel = 1

        def __str__(self) -> str:
            return super().__str__()
