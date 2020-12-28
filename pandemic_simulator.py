import json
import random


# Variables iniciales
with open('virus.json') as f:
	data = json.load(f)
inputs = data[0]
radius = inputs['Radius']
cont_prob = inputs['Contagious_prob']
death_rate = inputs['Death_rate']
poblacion = inputs['Initial_population']
heal_days = inputs['Days_to_heal']
