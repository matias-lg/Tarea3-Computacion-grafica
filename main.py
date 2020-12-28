import json

with open('virus.json') as f:
	data = json.load(f)

print(data)

for i in [1,2,3,4]:
	print(i)