import json
import sys
from modelos import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

if __name__ == "__main__":
	settings = sys.argv[1]
# Variables iniciales desde el archivo json
with open(str(settings)) as f:
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
sanos_diarios = []
enfermos_diarios = []
data_diario = []
dias = []
normales = []
contagios = []
recuperados = []
muertos = []
print("Simulando...")
while True:
    #  datos diarios
    sanos = sim._sim.getPositions()
    enfermos = sim._sim.getInfectedPositions()
    sanos_diarios += [[(i[0],i[1]) for i in sanos]]
    enfermos_diarios += [[(i[0],i[1]) for i in enfermos]]
    # Simulamos el dia actual
    data = sim.Simulate()
    # actualizamos posiciones / estados
    sim._sim.update()
    # actualiza arreglos para el grafico acumulado
    dia+=1
    data_diario.append(data)
    dias.append(dia)
    normales.append(data[3])
    contagios.append(data[4])
    recuperados.append(data[5])
    muertos.append(data[6])

    if len(enfermos) == 0:
        cnt += 1
    if cnt > heal_days + 1:
        break

# Figura inicial (dia 0)
fig, ax = plt.subplots()
plt.figure(0)
sanosIni = sanos_diarios[0]
enfermosIni = enfermos_diarios[0]
plt.subplots_adjust(bottom=0.2)
s, = plt.plot([i[0] for i in sanosIni], [i[1] for i in sanosIni], '.', color='blue', markersize=5)
e, = plt.plot([i[0] for i in enfermosIni], [i[1] for i in enfermosIni], '.', color='red',markersize=5)
plt.xlim(0, 1)
plt.ylim(0, 1)
class Indice(object):
	def __init__(self):
		self.ind = 0
	def next(self, event):
		try:
			sanos_diarios[self.ind+1]
		except:
			return
		self.ind += 1
		sanos_hoy = sanos_diarios[self.ind]
		enfermos_hoy = enfermos_diarios[self.ind]
		# sanos
		x_san = [pos[0] for pos in sanos_hoy]
		y_san = [pos[1] for pos in sanos_hoy]
		s.set_xdata(x_san)
		s.set_ydata(y_san)
		# enfermos
		x_enf = [pos[0] for pos in enfermos_hoy]
		y_enf = [pos[1] for pos in enfermos_hoy]
		e.set_xdata(x_enf)
		e.set_ydata(y_enf)
		plt.draw()

	def prev(self,event):
		if self.ind == 0:
			return
		self.ind -= 1
		sanos_hoy = sanos_diarios[self.ind]
		enfermos_hoy = enfermos_diarios[self.ind]
		# sanos
		x_san = [pos[0] for pos in sanos_hoy]
		y_san = [pos[1] for pos in sanos_hoy]
		s.set_xdata(x_san)
		s.set_ydata(y_san)
		# enfermos
		x_enf = [pos[0] for pos in enfermos_hoy]
		y_enf = [pos[1] for pos in enfermos_hoy]
		e.set_xdata(x_enf)
		e.set_ydata(y_enf)
		plt.draw()
	def info(self, event):
		i = self.ind
		enfermos_acc = 1
		muertos_acc = 0
		rec_acc = 0
		for k in range(i):
			rec_acc += data_diario[k][1]
			muertos_acc += data_diario[k][2]
			enfermos_acc += data_diario[k][0]
		sanos_print = len(sanos_diarios[i])-rec_acc
		if sanos_print < 0: sanos_print = 0
		print("REPORTE DIARIO (dia "+str(i)+"): ")
		if i == 0:
			print("Nuevos casos: 1")
			print("Fallecidos hoy: 0")
			print("Personas recuperadas hoy: 0")
		else:
			print("Nuevos casos: " + str(data_diario[i-1][0]))
			print("Fallecidos hoy: " + str(data_diario[i-1][2]))
			print("Personas recuperadas hoy: " + str(data_diario[i-1][1]))
		print("----------------------------------------")
		print("Personas sanas [TOTAL/HOY]: " + str(sanos_print))
		print("Personas enfermas [TOTAL]: " + str(enfermos_acc))
		print("Personas muertas [TOTAL]: " + str(muertos_acc))
		print("Personas recuperadas [TOTAL]: "+ str(rec_acc))
		print("////////////////////////////////////////")

callback = Indice()
axnext = plt.axes([0.7, 0.05, 0.2, 0.075])
axprev = plt.axes([0.48, 0.05, 0.2, 0.075])
axprint = plt.axes([0.26, 0.05, 0.2, 0.075])
bnext = Button(axnext, 'Dia siguiente')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Dia anterior')
bprev.on_clicked(callback.prev)
bprint = Button(axprint, 'Reporte diario')
bprint.on_clicked(callback.info)
plt.figure(1)
plt.xlabel("Dias desde el primer caso")
plt.ylabel("Cantidad de personas")
plt.plot(dias, normales, label="Personas no contagiadas")
plt.plot(dias, contagios, label="Personas contagiadas")
plt.plot(dias, recuperados, label="Personas recuperadas (inmunes)")
plt.plot(dias, muertos, label="Personas fallecidas")
plt.legend()
plt.draw()
plt.show()
