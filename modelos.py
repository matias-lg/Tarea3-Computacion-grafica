import random
import numpy as np

class Person(object):
    def __init__(self):
        self._pos = [random.random(), random.random()]
        self._infected = False
        self._dead = False
        self._inmune = False

    def getPos(self):
        return self._pos
    # movemos a las personas aleatoriamente
    def move(self):
        oldx = self._pos[0]
        oldy = self._pos[1]
        if random.random() >= 0.5:
            self._pos[0] += random.uniform(0.01, 0.08)
        else:
            self._pos[0] -= random.uniform(0.01, 0.08)
        if random.random() >= 0.5:
            self._pos[1] += random.uniform(0.01, 0.08)
        else:
            self._pos[1] -= random.uniform(0.01, 0.08)
        # Personas deben estar dentro del cuadrado [0,1]x[0,1]
        if not (0 <= self._pos[0] <= 1 and 0 <= self._pos[1] <= 1):
            self._pos[0] = oldx
            self._pos[1] = oldy
            self.move()


    def isInfected(self):
        return self._infected

    def infect(self):
        self._infected = True
        self._days = 0

    def die(self):
        self._dead = True
        self._infected = False

    def isDead(self):
        return self._dead

    def isInmune(self):
        return self._inmune

    def recover(self):
        self._days += 1
        return self._days

    def sanar(self):
        self._days = 0
        self._infected = False
        self._inmune = True


class PersonGenerator(object):
    def __init__(self):
        self._people = []
        self._infected_people = []
        self._positions = []
        self._infecteds_positions = []
        self._inmune_positions = []
        self._days = 0

    def generate(self, n):
        for i in range(n):
            tmp = Person()
            # Siempre habra solo un infectado al inicio
            if i == 1:
                tmp.infect()
            self._people.append(tmp)

    def update(self):
        self._infected_people = []
        self._positions = []
        self._infecteds_positions = []
        #self._inmune_positions = []
        for person in self._people:
            if person.isDead():
                pass
            elif person.isInfected() and not person.isDead():
                self._infected_people.append(person)
                self._infecteds_positions.append(person.getPos())
            # elif person.isInmune():
            #     self._inmune_positions.append(person.getPos())
            else:
                self._positions.append(person.getPos())
        return [self._positions, self._infecteds_positions]

    def getPeople(self):
        return self._people

    def setPeople(self, people_arr):
        self._people = people_arr

    def getInfectedPeople(self):
        return self._infected_people

    def setInfectedPeople(self, inf_arr):
        self._infected_people = inf_arr

    def getInmunePositions(self):
        return self._inmune_positions

    def getPositions(self):
        return self._positions

    def getInfectedPositions(self):
        return self._infecteds_positions

    def addInfected(self, person):
        assert person is Person
        person.infect()
        self._infecteds_positions.append(person.getPos())


class Simulator(object):
    def __init__(self, Radius, Contagious_prob, Death_rate, Initial_population, Days_to_heal):
        self._sim = PersonGenerator()
        self._sim.generate(Initial_population)
        self._sim.update()
        self._r = Radius
        self._cont_prob = Contagious_prob
        self._death_rate = Death_rate
        self._n = Initial_population
        self._heal_time = Days_to_heal
        self._infected_count = 1
        self._normal_count = Initial_population - 1
        self._death_count = 0
        self._healed_count = 0

    def Simulate(self):
        infected_count_HOY = 0
        healed_count_HOY = 0
        death_count_HOY = 0
        self._sim.update()
        sim = self._sim
        people = sim.getPeople()
        infected_people = sim.getInfectedPeople()
        # Revisamos si hay personas cerca del enfermo, luego se contagia con probabilidad Contagious_prob
        for enfermo in infected_people:
            for person in people:
                if not enfermo.isDead():
                    if enfermo is not person and not person.isDead() and not person.isInfected() and not person.isInmune():
                        if np.linalg.norm(np.asarray(enfermo.getPos()) - np.asarray(person.getPos())) <= self._r and random.random() <= self._cont_prob:
                            person.infect()
                            self._infected_count += 1
                            infected_count_HOY += 1
                            self._normal_count -= 1
        # Las personas se mueven aleatoriamente
        for person in people:
            person.move()
        for person in infected_people:
            if not person.isDead():
                # Mueren segun death rate
                if person.isInfected():
                    if random.random() <= self._death_rate and not person.isDead():
                        person.die()
                        if self._infected_count > 0:
                            self._death_count += 1
                            death_count_HOY += 1
                            self._infected_count -= 1
                # Si pasan los dias necesarios se sanan
                    if person.recover() >= self._heal_time and not person.isInmune():
                        person.sanar()
                        if self._infected_count > 0:
                            self._infected_count -= 1
                            self._healed_count += 1
                            healed_count_HOY += 1
        self._sim.setPeople(people)
        self._sim.setInfectedPeople(infected_people)
        return [infected_count_HOY, healed_count_HOY, death_count_HOY, self._normal_count, self._infected_count,
                self._healed_count, self._death_count]

    def printInfo(self):
        print("Personas sanas [TOTAL/HOY]: " + str(self._normal_count))
        print("Personas enfermas [TOTAL]: " + str(self._infected_count))
        print("Personas muertas [TOTAL]: " + str(self._death_count))
        print("Personas recuperadas [TOTAL]: " + str(self._healed_count))
        print("Total: " + str(self._normal_count +
                              self._infected_count + self._death_count + self._healed_count))
