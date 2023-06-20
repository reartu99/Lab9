import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def media_varianza_min_max(arr):
    print("La media è:", np.mean(arr))
    print("La varianza è:", np.var(arr))
    print("La stdev è:", np.std(arr))
    print("Il massimo ed il minimo valore registrati sono:", max(arr), min(arr))
    print("")
    print("")
    return np.mean(arr)


def histog(arr, orient, nome):
    nbins = int(np.ceil(np.log2(len(arr)))) + 1  # Scegliamo il numero di bins con la regola di Stourges

    if orient == 1:
        colors = 'red'
    else:
        colors = 'blue'

    plt.hist(arr, bins=nbins, color=colors)
    plt.title("Distanza " + nome[5:7:] + " cm " + "configurazione " + nome[11:12:])
    plt.show()
    print("Distanza (cm): " + nome[5:7:])


def apri(nome, orient, medie):
    df = pd.read_csv(nome, on_bad_lines='skip')
    colonna = df['Ultimo']
    histog(colonna, orient, nome)
    value = media_varianza_min_max(colonna)
    medie.append(value)
    return colonna


def linee(ranges, t11, t12, t22, t21, x1, x2):
    linearossa = []
    lineablue = []
    for x in ranges:
        linearossa.append(((t21 - t11) / (x2 - x1)) * (x - x1) + t11)
    for x in ranges:
        lineablue.append(((t22 - t12) / (x2 - x1)) * (x - x1) + t12)
    return linearossa, lineablue


def find_line_intersection(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    #  Si calcola intercette e slope dati 2 punti per linea
    #  I punti sono p1 che è il primo punto della linea blu, p2 il secodo punto della linea blue
    #  p3 il primo punto della linea rossa e p4 il secondo punto della linea rossa
    m1 = float((y2 - y1) / (x2 - x1))
    b1 = y1 - m1 * x1

    m2 = float((y4 - y3) / (x4 - x3))
    b2 = y3 - m2 * x3

    if np.isclose(m1, m2):
        print(m1, m2)
        print("Linee parallele!")
        return None

    # Calculate the x-coordinate of the intersection point
    x_intersez = (b2 - b1) / (m1 - m2)

    # Calculate the y-coordinate of the intersection point
    y_interez = m1 * x_intersez + b1

    print("Tstar è:", y_interez)

    return x_intersez, y_interez


meds = []
intervalli = [35, 36, 37, 39]

apri("venv/35conf1.csv", 1, meds)
apri("venv/35conf2.csv", 2, meds)
apri("venv/36conf1.csv", 1, meds)
apri("venv/36conf2.csv", 2, meds)
apri("venv/37conf1.csv", 1, meds)
apri("venv/37conf2.csv", 2, meds)
apri("venv/39conf1.csv", 1, meds)
apri("venv/39conf2.csv", 2, meds)

#  Questa funcione plotta _E_ mette le barre di errore sui punti che plotta
plt.errorbar(intervalli, meds[::2], xerr=0.1, fmt='o')
plt.errorbar(intervalli, meds[1::2], xerr=0.1, fmt='o', color='red')

lrossa, lblue = linee(intervalli, meds[0], meds[1], meds[3], meds[4], 35, 36)

p1 = (intervalli[0], meds[0])
p2 = (intervalli[1], meds[2])
p3 = (intervalli[0], meds[1])
p4 = (intervalli[1], meds[3])
tstar = find_line_intersection(p1, p2, p3, p4)

plt.plot(tstar[0], tstar[1], '*k', label="Punto di intersezione")
plt.plot(intervalli, lrossa, color='#f07167')
plt.plot(intervalli, lblue, color='#0096c7')
plt.show()

print("Da cui ricaviamo g: ", 4*np.pi**2*0.994/(tstar[1]**2))
