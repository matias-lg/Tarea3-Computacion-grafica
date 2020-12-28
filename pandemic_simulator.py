import json

# Variables iniciales
with open('virus.json') as f:
	data = json.load(f)
inputs = data[0]
radius = inputs['Radius']
prob_con = inputs['Contagious_prob']
death_rate = inputs['Death_rate']
poblacion = inputs['Initial_population']
heal_days = inputs['Days_to_heal']

print(radius, prob_con, death_rate, poblacion, heal_days)
