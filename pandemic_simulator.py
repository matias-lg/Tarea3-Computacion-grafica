import json
import sys
from modelos import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tplotOPENGL as top

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

# Simulador dados los parametros desde el archivo .json
sim = Simulator(radius, cont_prob, death_rate, poblacion, heal_days)

# Arreglos y variables que guardan los datos
cnt = 0
dia = 0
sanos_diarios = []
enfermos_diarios = []
data_diario = []
dias = []
normales = []
contagios = []
recuperados = []
muertos = []

# Simula todo el virus
print("Simulando...")
while True:
    #  datos diarios
    sanos = sim._sim.getPositions()
    enfermos = sim._sim.getInfectedPositions()
    sanos_diarios += [[(i[0], i[1]) for i in sanos]]
    enfermos_diarios += [[(i[0], i[1]) for i in enfermos]]
    # Simulamos el dia actual
    data = sim.Simulate()
    # actualizamos posiciones / estados
    sim._sim.update()
    # actualiza arreglos para el grafico acumulado
    dia += 1
    data_diario.append(data)
    dias.append(dia)
    normales.append(data[3])
    contagios.append(data[4])
    recuperados.append(data[5])
    muertos.append(data[6])
    # Llegamos al fin, ultimo contagio + tiempo de recuperacion
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
s, = plt.plot([i[0] for i in sanosIni], [i[1]
                                         for i in sanosIni], '.', color='blue', markersize=5)
e, = plt.plot([i[0] for i in enfermosIni], [i[1]
                                            for i in enfermosIni], '.', color='red', markersize=5)
plt.xlim(0, 1)
plt.ylim(0, 1)
# Controlador, los botones en la UI usaran estos metodos


class Indice(object):
    def __init__(self):
        self.ind = 0
    # Avanzar un dia

    def next(self, event):
        try:
            sanos_diarios[self.ind + 1]
        except:
            return
        # Mostrar el dia
        self.ind += 1
        print("DIA " + str(self.ind))
        # actualizar todas las posiciones en un dia
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
    # Ir un dia hacia atras

    def prev(self, event):
        if self.ind == 0:
            return
        # mostrar el dia
        self.ind -= 1
        print("DIA " + str(self.ind))
        # actualizar todas las posiciones en un dia
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
    # Muestra recuento diario y acumulado

    def info(self, event):
        i = self.ind
        enfermos_acc = 1
        muertos_acc = 0
        rec_acc = 0
        for k in range(i):
            rec_acc += data_diario[k][1]
            muertos_acc += data_diario[k][2]
            enfermos_acc += data_diario[k][0]
        sanos_print = len(sanos_diarios[i]) - rec_acc
        if sanos_print < 0:
            sanos_print = 0
        print("----------------------------------------")
        print("REPORTE DIARIO (dia " + str(i) + "): ")
        if i == 0:
            print("Nuevos casos: 1")
            print("Fallecidos hoy: 0")
            print("Personas recuperadas hoy: 0")
        else:
            print("Nuevos casos: " + str(data_diario[i - 1][0]))
            print("Fallecidos hoy: " + str(data_diario[i - 1][2]))
            print("Personas recuperadas hoy: " + str(data_diario[i - 1][1]))
        print("----------------------------------------")
        print("Personas sanas [TOTAL/HOY]: " + str(sanos_print))
        print("Personas enfermas [TOTAL]: " + str(enfermos_acc))
        print("Personas muertas [TOTAL]: " + str(muertos_acc))
        print("Personas recuperadas [TOTAL]: " + str(rec_acc))
        print("----------------------------------------\n")
    # Muestra ventana con grafico generado en OpenGL para el dia de hoy

    def showGL(self, event):
        # obtener angulos y colores
        i = self.ind
        enfermos_acc = 1
        muertos_acc = 0
        rec_acc = 0
        for k in range(i):
            rec_acc += data_diario[k][1]
            muertos_acc += data_diario[k][2]
            enfermos_acc += data_diario[k][0]
        sanos_acc = len(sanos_diarios[i]) - rec_acc
        enfermos_acc -= muertos_acc + rec_acc
        # calcular porcentajes para el grafico
        tot = enfermos_acc + muertos_acc + rec_acc + sanos_acc
        ps = sanos_acc / tot
        pcont = enfermos_acc / tot
        pm = muertos_acc / tot
        prec = rec_acc / tot
        # dibujar
        # sanos, contagiados, muertos, inmunes
        top.draw(ps, pcont, pm, prec)
    # Grafico completo del virus durante toda su duracion

    def grafoFinal(self, event):
        plt.figure(1)
        plt.title("Virus a lo largo del tiempo")
        plt.xlabel("Dias desde el primer caso")
        plt.ylabel("Cantidad de personas")
        plt.plot(dias, normales, label="Personas no contagiadas")
        plt.plot(dias, contagios, label="Personas contagiadas")
        plt.plot(dias, recuperados, label="Personas recuperadas (inmunes)")
        plt.plot(dias, muertos, label="Personas fallecidas")
        plt.legend()
        plt.draw()
        plt.show()


# creamos el controlador
callback = Indice()
# Dimensiones y posiciones de los botones
axnext = plt.axes([0.7, 0.05, 0.2, 0.075])
axprev = plt.axes([0.48, 0.05, 0.2, 0.075])
axprint = plt.axes([0.26, 0.05, 0.2, 0.075])
axgl = plt.axes([0.005, 0.05, 0.24, 0.075])
axf = plt.axes([0.7, 0.90, 0.2, 0.075])
# Conectamos los botones con el controlador
bnext = Button(axnext, 'Dia siguiente')
bnext.on_clicked(callback.next)

bprev = Button(axprev, 'Dia anterior')
bprev.on_clicked(callback.prev)

bprint = Button(axprint, 'Reporte diario')
bprint.on_clicked(callback.info)

bgl = Button(axgl, 'Grafico diario OpenGL')
bgl.on_clicked(callback.showGL)

bfinal = Button(axf, 'Acumulado final')
bfinal.on_clicked(callback.grafoFinal)

plt.close(1)
plt.show()
