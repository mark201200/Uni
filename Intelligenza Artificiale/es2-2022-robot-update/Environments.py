import random

from FallingObjects import *


class Environment:

    def __init__(self, width, height, agent):
        self.width = width
        self.height = height
        self.agent = agent
        self.agent.env = self
        self.rock = self.generateObject("rock")
        self.energy = self.generateObject("energy")
        self.floor = [8] * width

        self.totalRockDamage = 0  ##TODO meglio?
        self.round = 0

    def fall(self):  # function per far cadere roccia e energia
        self.rock.y = self.rock.y - self.rock.vel
        self.energy.y = self.energy.y - 1

    def checkCollisions(self):  # controlla se uno degli oggetti ha colpito il pavimento o l'agente

        # controllo se è caduta una roccia
        if self.rock.y == 0:
            if self.agent.x == self.rock.x:  # se l'agente e la roccia hanno stessa colonna rigenero la roccia
                self.rock = self.generateObject("rock")
        elif self.rock.y < 0:
            self.floor[self.rock.x] -= self.rock.dmg  # se l'agente non interviene il pavimento viene danneggiato
            self.rock = self.generateObject("rock")

        # controllo se l'energia è caduta
        if self.energy.y == 0:
            if self.agent.x == self.energy.x:  # se l'agente e l'energia hanno stessa colonna rigenero l'energia
                self.agent.restoreEnergy()  # rigenero l'energia dell'agente
                self.energy = self.generateObject("energy")
        elif self.energy.y < 0:
            self.energy = self.generateObject("energy")

    def generateObject(self, type):
        if type == "rock":
            self.obj = Rock(random.randint(0, self.width - 1), self.height - 1, random.choice([1, 2, 5]))
        else:
            self.obj = Energy(random.randint(0, self.width - 1), self.height - 1)

        return self.obj

    def lost(self):
        for floorHealth in self.floor:
            if floorHealth <= 0:
                return True
        return False

    def percept(self):
        return self.rock, self.energy, self.floor

    def execute(self, action):
        if action == 'right' and self.agent.x < self.width - 1:
            self.agent.move(action)
        elif action == 'left' and self.agent.x > 0:
            self.agent.move(action)
        elif action == 'none':
            pass

    def step(self, manualExec=None):  # è un tick time dell'enviroment, restituisce false se è distrutto il pavimento
        if self.lost():
            print("Hai perso????")
            return False

        self.round += 1
        self.fall()
        self.checkCollisions()
        self.execute(self.agent.program(self.percept()))

        return True

    def __str__(self):
        round = "Round: " + str(self.round) + "\n"
        obj = str(self.agent) + "\n" + str(self.rock) + "\n" + str(self.energy)
        env = ""
        for y in reversed(range(self.height+1)):
            for x in range(self.width):
                if self.agent.x == x and y == 0:
                    env = env + 'A '
                elif self.energy.x == x and self.energy.y == y:
                    env = env + 'E '
                elif self.rock.x == x and self.rock.y == y:
                    env = env + str(self.rock.dmg) + ' '
                else:
                    env = env + '. '
            env = env + '\n'
        floor = ""
        for x in self.floor:
            floor = floor + str(x) + ' '
        return '\n\n\n' + round + obj + env + floor + '\n\n\n'
