import random


class Object:                                   #La classe oggetto, serve per rappresentare l'energia e la roccia

    def __init__(self, type, x, y, damage=0):
        self.type = type
        self.damage = damage
        self.x = x
        self.y = y


class Environment:                              #La classe ambiente, contiene tutte le variabili e le funzioni di base
    def __init__(self, width, height):
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

    def placeObj(self, obj):                    #Funzione per posizionare l'energia o la roccia automaticamente
        x = random.randint(0, self.width - 1)
        if obj.type == "energy":
            obj.x = x
            obj.y = self.height - 1
        elif obj.type == "rock":
            obj.x = x
            obj.y = self.height - 1
            obj.damage = random.choice([1, 2, 5])

    def fall(self):                             #Funzione per far cadere la roccia e l'energia
        if self.energy.y > 0:
            self.energy.y -= 1
        else:
            self.energyCheck()
            self.placeObj(self.energy)

        if self.rock.y >= 1 and self.rock.damage != 1:
            self.rock.y -= 2
        elif self.rock.y >= 0 and self.rock.damage == 1:
            self.rock.y -= 1
        else:
            self.floorDamage()
            self.placeObj(self.rock)

    def floorDamage(self):                      #Funzione che calcola il danno al pavimento
        if self.agent.x != self.rock.x:
            self.floor[self.rock.x] -= self.rock.damage
            print("Floor tile ", self.rock.x, " damaged by ", self.rock.damage, " units")
        else:
            print("Agent shielded the floor!")

    def energyCheck(self):                      #Funzione che controlla se l'energia è stata raccolta
        if self.agent.x == self.energy.x and self.agent.y == self.energy.y:
            self.agent.restoreEnergy()
            print("Agent energy restored!")

    def isDone(self):                           #Funzione che controlla se ho perso
        for floorEnergy in self.floor:
            if floorEnergy <= 0:
                print("Game Over")
                return True

    def print(self):                           #Funzione per stampare l'ambiente
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

        print()
        print()

    def step(self):                                 #Funzione che esegue un passo
        self.round += 1
        action = self.agent.program(self.percept())
        self.execute(action)
        self.fall()
        if self.isDone():
            return False
        return True

    def percept(self):                              #Funzione che restituisce i valori di percezione
        return self.rock, self.energy

    def execute(self, action):                      #Funzione che esegue l'azione scelta dall'agente
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

    def program(self, percept):                     #Funzione che contiene il programma dell'agente
        rock, energy = percept
        if rock.y == -1:
            return 'none'
        if self.energy <= 10 and rock.damage == 1 and self.reachable(energy) and self.env.floor[rock.x] > 1:
            print("Prioritizing energy. Moving", self.direction(energy), "towards energy")
            return self.direction(energy)
        if self.reachable(rock):
            print("Rock is reachable. Moving", self.direction(rock))
            return self.direction(rock)
        elif self.reachable(energy):
            print("Rock is NOT reachable. Moving", self.direction(energy), "to get energy")
            return self.direction(energy)
        else:
            print("Nothing is reachable. Moving", self.direction(rock), "towards center")
            if self.x < 4:
                return 'right'
            elif self.x > 5:
                return 'left'

    def direction(self, obj):             #Funzione che restituisce la direzione da prendere per raggiungere un oggetto
        if self.x < obj.x:
            return 'right'
        elif self.x > obj.x:
            return 'left'
        else:
            return 'none'

    def reachable(self, obj):                               #Funzione che controlla se un oggetto è raggiungibile
        if self.getDistanceX(obj) <= self.getDistanceY(obj):
            if self.getDistanceX(obj) <= self.energy:
                return True
            else:
                return False
        else:
            return False

    def getDistanceX(self, obj):                   #Funzione che restituisce la distanza tra l'agente e un oggetto in x
        return abs(self.x - obj.x)

    def getDistanceY(self, obj):                   #Funzione che restituisce la distanza tra l'agente e un oggetto in y
        if obj.type == "energy":
            return obj.y
        else:
            return obj.y / 2

    def restoreEnergy(self):                        #Funzione che ripristina l'energia
        self.energy = 20

    def move(self, direction):                      #Funzione che fa muovere l'agente se ha energia
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
        # input("Press Enter to continue...")
