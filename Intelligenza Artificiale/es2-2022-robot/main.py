## Esercizio Robot - Altomare - Santuci
import copy
import random


class Object:  # La classe oggetto, serve per rappresentare l'energia e la roccia

    def __init__(self, type, x, y, damage=0):
        self.type = type
        self.damage = damage
        self.x = x
        self.y = y


class Environment:  # La classe ambiente, contiene tutte le variabili e le funzioni di base

    def __init__(self, width, height):
        self.totalRockDamage = 0
        self.noprint = 0
        self.round = 0
        self.width = width
        self.height = height
        self.rock = Object("rock", 0, 0, 0)
        self.energy = Object("energy", 0, 0)
        self.placeObj(self.rock)
        self.placeObj(self.energy)
        self.floor = []
        for i in range(width):
            self.floor.append(8)
        self.agent = None

    def placeObj(self, obj):  # Funzione per posizionare l'energia o la roccia automaticamente
        x = random.randint(0, self.width - 1)
        if obj.type == "energy":
            obj.x = x
            obj.y = self.height - 1
        elif obj.type == "rock":
            obj.x = x
            obj.y = self.height - 1
            obj.damage = random.choice([1, 2, 5])
            self.totalRockDamage += obj.damage

    def fall(self):  # Funzione per far cadere la roccia e l'energia
        if self.energy.y > 0:
            self.energy.y -= 1
        else:
            self.energyCheck()
            self.placeObj(self.energy)

        if self.rock.y >= 1 and self.rock.damage != 1:
            self.rock.y -= 2
        elif self.rock.y > 0:
            self.rock.y -= 1
        else:
            self.floorDamage()
            self.placeObj(self.rock)

    def floorDamage(self):  # Funzione che calcola il danno al pavimento
        if self.agent.x != self.rock.x:
            self.floor[self.rock.x] -= self.rock.damage
            if self.noprint == 0:
                print("Floor tile ", self.rock.x, " damaged by ", self.rock.damage, " units")
        else:
            if self.noprint == 0:
                print("Agent shielded the floor!")

    def energyCheck(self):  # Funzione che controlla se l'energia è stata raccolta
        if self.agent.x == self.energy.x and self.agent.y == self.energy.y:
            self.agent.restoreEnergy()
            if self.noprint == 0:
                print("Agent energy restored!")

    def isDone(self):  # Funzione che controlla se ho perso
        for floorEnergy in self.floor:
            if floorEnergy <= 0:
                if self.noprint == 0:
                    print("Floor compromised! Game over")
                return True

    def print(self):  # Funzione per stampare l'ambiente
        print()
        print("Total rock damage: ", self.totalRockDamage)
        print("Round: ", self.round)
        print("Agent Location: ", self.agent.x)
        print("Agent Energy: ", self.agent.energy)
        print("Rock Location: ", self.rock.x, self.rock.y)
        print("Energy Location: ", self.energy.x, self.energy.y)
        print("Floor Energy: ", self.floor)
        for y in reversed(range(self.height)):
            for x in range(self.width):
                if self.agent.x == x and self.agent.y == y:
                    print('A ', end='')
                elif self.energy.x == x and self.energy.y == y:
                    print('E ', end='')
                elif self.rock.x == x and self.rock.y == y:
                    print(str(self.rock.damage) + ' ', end='')
                else:
                    print('. ', end='')
            print()

        for tile in self.floor:
            print(tile, end=' ')
        print()

    def step(self, forced='notSp'):  # Funzione che esegue un passo, forced serve per la simulazione
        self.round += 1
        if forced == 'notSp':
            action = self.agent.program(self.percept())
            self.execute(action)
        else:
            self.noprint = 1
            self.execute(forced)
        self.fall()
        if self.isDone():
            return False
        return True

    def percept(self):  # Funzione che restituisce i valori di percezione
        return self.rock, self.energy

    def execute(self, action):  # Funzione che esegue l'azione scelta dall'agente
        if action == 'right' and self.agent.x < self.width - 1:
            self.agent.move(action)
        elif action == 'left' and self.agent.x > 0:
            self.agent.move(action)
        elif action == 'none':
            pass


class Agent:
    def __init__(self, name, environment):
        self.name = name
        self.env = environment
        self.env.agent = self
        self.x = 5
        self.y = 0
        self.energy = 20

    def utilityFn(self, environment=None):
        if environment is None:
            environment = self.env
        rock, energy = environment.percept()
        agent = environment.agent
        #utility = (((rock.damage / 5) / ((agent.getDistanceX(rock) + agent.getDistanceY(rock)) + 1)) * 1 ) + ((
        #        abs((agent.energy / 20) - 1) / ((agent.getDistanceX(energy) + agent.getDistanceY(energy)) + 1)) * 1)

        utility = (((rock.damage / 5) / ((agent.getDistanceX(rock) / (agent.getDistanceY(rock) + 1))+1)) + ((
                abs((agent.energy / 20) - 1) / ((agent.getDistanceX(energy) / (agent.getDistanceY(energy) + 1))+1))))

        return utility

    def simulateMovementUtil(self, action):  # Simulazione di un movimento, e ritorno della funzione utilità.
        simulatedEnv = copy.deepcopy(self.env)
        simulatedEnv.step(action)
        return self.utilityFn(simulatedEnv)

    def program(self, percept):  # Funzione che contiene il programma dell'agente
        rock, energy = percept

        if rock.y <= 0 and self.x == rock.x:
            print("Rock destroyed!")
            return 'none'

        if energy.y <= 0 and self.x == energy.x:
            print("Energy collected!")
            return 'none'

        scoreRight = self.simulateMovementUtil('right')
        scoreLeft = self.simulateMovementUtil('left')
        scoreNone = self.simulateMovementUtil('none')

        print("Score movimento sinistra: ", scoreLeft, "Score movimento destra: ",
              scoreRight, "Score no movimento: ", scoreNone)

        if scoreRight > scoreLeft and scoreRight > scoreNone:
            print("Spostamento a destra")
            return 'right'
        elif scoreLeft > scoreRight and scoreLeft > scoreNone:
            print("Spostamento a sinistra")
            return 'left'
        else:
            print("Nessun spostamento")
            return 'none'

    def center(self):
        if self.x < 4:
            return 'right'
        elif self.x > 5:
            return 'left'

    def direction(self, obj):  # Funzione che restituisce la direzione da prendere per raggiungere un oggetto
        if self.x < obj.x:
            return 'right'
        elif self.x > obj.x:
            return 'left'
        else:
            return 'none'

    def reachable(self, obj):  # Funzione che controlla se un oggetto è raggiungibile e se ho abbastanza energia
        if (self.getDistanceX(obj) <= self.getDistanceY(obj)) and (self.getDistanceX(obj) <= self.energy):
            return True
        else:
            return False

    def getDistanceX(self, obj):  # Funzione che restituisce la distanza tra l'agente e un oggetto in x
        return abs(self.x - obj.x)

    def getDistanceY(self, obj):  # Funzione che restituisce la distanza tra l'agente e un oggetto in y
        if obj.type == "energy" or obj.damage == 1:
            return obj.y
        else:
            return obj.y / 2

    def restoreEnergy(self):  # Funzione che ripristina l'energia
        self.energy = 20

    def move(self, direction):  # Funzione che fa muovere l'agente se ha energia
        if self.energy > 0:
            if direction == 'left':
                self.x -= 1
                self.energy -= 1
            elif direction == 'right':
                self.x += 1
                self.energy -= 1


if __name__ == '__main__':
    env = Environment(10, 10)
    agent = Agent("Robottino", env)
    while True:
        env.print()
        if not env.step():
            break
        #input("Press Enter to step...")
