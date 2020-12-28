import random
import pandemic_simulator
class Person(object):
	def __init__(self):
		self._pos = (random.random(),random.random())
		self._infected = False
		self._dead = False

	def getPos(self):
		return self._pos
	def move(self):
		if random.random() >= 0.5:
			self._pos[0] += random.uniform(0.5,0.1)
		else:
			self._pos[0] -= random.uniform(0.5,0.1)
		if random.random() >= 0.5:
			self._pos[1] += random.uniform(0.5,0.1)
		else:
			self._pos[1] -= random.uniform(0.5,0.1)
	def isInfected(self):
		return self._infected
	def infect(self):
		self._infected = True 

class PersonGenerator(object):
	def __init__(self):
		self._people = []
		self._positions = []
		self._infecteds_positions = []
	def generate(self, n):
		for i in range(n):
			tmp = Person()
			# Siempre habra solo un infectado al inicio
			if i == 1:
				tmp.infect()
			self._people.append(tmp)
	def updatePositions(self):
		self._infecteds_positions = []
		self._infecteds_positions = []
		for person in self._people:
			if person.isInfected():
				self._infecteds_positions.append(person.getPos())
			self._positions.append(person.getPos())
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
		self._sim()
		self._r = Radius
		self._cont_prob = Contagious_prob
		self._death_rate = Death_rate
		self._n = Initial_population
		self._heal_time = Days_to_heal
	def Simulate(self):
		sim = self._sim
		people = sim.getPositions()
		infected_people = sim.getInfectedPositions()


