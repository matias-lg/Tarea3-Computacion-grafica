import json

with open('virus.json') as f:
	data = json.load(f)

print(data)