import json
import sys
from modelos import *
import matplotlib.pyplot as plt
# if __name__ == "__main__":
# 	settings = sys.argv[1]
# Variables iniciales desde el archivo json
with open("virus.json") as f:
    data = json.load(f)
inputs = data[0]
radius = inputs['Radius']
cont_prob = inputs['Contagious_prob']
death_rate = inputs['Death_rate']
poblacion = inputs['Initial_population']
heal_days = inputs['Days_to_heal']
cnt = 0
dia = 0
sim = Simulator(radius, cont_prob, death_rate, poblacion, heal_days)
dias = []
normales = []
contagios = []
recuperados = []
muertos = []


while True:
    #  graficar
    sanos = sim._sim.getPositions()
    enfermos = sim._sim.getInfectedPositions()
    plt.scatter([i[0] for i in sanos], [i[1] for i in sanos], c='b', s=10)
    plt.scatter([i[0] for i in enfermos], [i[1]
                                           for i in enfermos], c='r', s=10)
    # Simulamos el dia actual
    data = sim.Simulate()
    # actualiza arreglos para el otro grafico
    dia += 1
    dias.append(dia)
    normales.append(data[3])
    contagios.append(data[4])
    recuperados.append(data[5])
    muertos.append(data[6])
    # actualizamos posiciones / estados
    sim._sim.update()
    # informacion en consola
    print("REPORTE DIARIO:")
    print("Nuevos casos: " + str(data[0]))
    print("Fallecidos hoy: " + str(data[2]))
    print("Personas recuperadas hoy: " + str(data[1]))
    print("----------------------------------------")
    sim.printInfo()
    print("////////////////////////////////////////")
    plt.pause(0.001)
    if len(enfermos) == 0:
        cnt += 1
    if cnt > heal_days + 1:
        break
    plt.clf()
plt.show()

# Grafico acumulado
plt.clf()
plt.xlabel("Dias desde el primer caso")
plt.ylabel("Cantidad de personas")
plt.plot(dias, normales, label="Personas no contagiadas")
plt.plot(dias, contagios, label="Personas contagiadas")
plt.plot(dias, recuperados, label="Personas recuperadas (inmunes)")
plt.plot(dias, muertos, label="Personas fallecidas")
plt.legend()
plt.show()
