class Agent:

    def __init__(self, name):
        self.name = name
        self.x = 5
        self.MAXENERGY = 20
        self.energy = self.MAXENERGY

    def restoreEnergy(self):
        self.energy = self.MAXENERGY

    def program(self, percept):
        rock, energy, floor = percept
        if rock.x == self.x:
            return 'stay'
        elif rock.x < self.x:
            return 'left'
        else:
            return 'right'

    def move(self, direction):  # Funzione che fa muovere l'agente se ha energia
        if self.energy > 0:
            if direction == 'left':
                self.x -= 1
                self.energy -= 1
            elif direction == 'right':
                self.x += 1
                self.energy -= 1

    def __str__(self):
        return "Agent: " + self.name + ", x = " + str(self.x) + ",energy = " + str(self.energy)
