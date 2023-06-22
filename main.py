import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.optimize import curve_fit


def properr(a, b, ea, eb):
    err = math.sqrt((ea/a)**2 + (eb/b)**2)
    return err


def properr2(ea, eb):
    err = math.sqrt(ea**2 + eb**2)
    return err


def media_varianza_min_max(arr):
    print("La media è:", np.mean(arr))
    print("La varianza è:", np.var(arr))
    print("La stdev è:", np.std(arr))
    print("Il massimo ed il minimo valore registrati sono:", max(arr), min(arr))
    print("")
    print("")
    return np.mean(arr)


def histog(arr, orient, nome):
    nbins = int(np.ceil(np.log2(len(arr))))  # Scegliamo il numero di bins con la regola di Stourges

    if orient == 1:
        colors = 'red'
    else:
        colors = 'blue'

    plt.hist(arr, bins=nbins, color=colors, alpha=0.5, histtype='bar', ec='black')
    plt.title("Distanza " + nome[5:7:] + " cm " + "configurazione " + nome[11:12:])
    plt.xlabel("tempi di oscillazione")
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


def deltatstr(medie):
    # x è 35 mentre meds[0] è t12
    # x è 36 mentre meds[2] è t22
    # x è 35 mentre meds[1] è t11
    # x è 36 mentre meds[3] è t21
    etstar = 0.00001 * ((properr2(medie[2]-medie[0], medie[3]-medie[1]) + properr2(medie[2]-medie[3], medie[0]-medie[1])) / (medie[2]-medie[3]-medie[0]+medie[1])**2)
    print("L'errore su tstar è:", etstar)
    return etstar


def curvfunc(a, b, t):
    return t*a+b


def curvfunc2(a, b, t):
    k = []
    for item in t:
        k.append(a*item + b)
    return k


def abline(slope, intercept):
    assi = plt.gca()
    x_vals = np.array(assi.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')


meds = []
intervalli = [35, 36, 37, 39]

print("")

print("Punto 3-4")
apri("venv/35conf1.csv", 1, meds)
apri("venv/35conf2.csv", 2, meds)
apri("venv/36conf1.csv", 1, meds)
apri("venv/36conf2.csv", 2, meds)
apri("venv/37conf1.csv", 1, meds)
apri("venv/37conf2.csv", 2, meds)
apri("venv/39conf1.csv", 1, meds)
apri("venv/39conf2.csv", 2, meds)

print("")

print("Punto 5")
#  Questa funcione plotta _E_ mette le barre di errore sui punti che plotta
#  yerr è l'errore dei fotogate che al momento mi sfugge
plt.errorbar(intervalli, meds[::2], xerr=0.2, yerr=0.00001, fmt='o', label='Peso aggiuntivo sul basso')
plt.errorbar(intervalli, meds[1::2], xerr=0.2, yerr=0.00001, fmt='o', color='red', label='Peso aggiuntivo in alto')
print("Questa funzione grafica e basta")
print("")

print("Punto 6")
lrossa, lblue = linee(intervalli, meds[0], meds[1], meds[3], meds[2], 35, 36)

p1 = (intervalli[0], meds[0])  # x è 35 mentre meds[0] è t12
p2 = (intervalli[1], meds[2])  # x è 36 mentre meds[2] è t22
p3 = (intervalli[0], meds[1])  # x è 35 mentre meds[1] è t11
p4 = (intervalli[1], meds[3])  # x è 36 mentre meds[3] è t21
print("Ecco i dati: ")
tstar = find_line_intersection(p1, p2, p3, p4)
etstar = deltatstr(meds)

#  plt.plot(intervalli, lrossa, color='#0096c7')
#  plt.plot(intervalli, lblue, color='#f07167')
#  plt.errorbar(tstar[0], tstar[1], marker='*', label="t*", color='k', xerr=0.2, yerr=etstar)
plt.legend(loc='best')
plt.xlabel("Distanza massa mobile (cm)")
plt.ylabel("Tempi di oscillazione (s)")
plt.show()

print("Da cui ricaviamo g: ", 4*np.pi**2*0.994/(tstar[1]**2))
print("")

print("Punto 9")

popt, pcov = curve_fit(curvfunc, meds[::2], intervalli)
xa, xb = popt
print("La prima curva è data da y =", xa, "x", "+", xb)
exa, exb = np.sqrt(np.diag(pcov))
print("Gli errori sono: ", exa, exb)
print("Il fattore di cov(A,B) è", pcov[0][1], "Mentre quello di cov(B,A) è", pcov[1][0])
popt2, pcov2 = curve_fit(curvfunc, meds[1::2], intervalli)
xa2, xb2 = popt2
print("La seconda curva è data da y =", xa2, "x", "+", xb2)
exa2, exb2 = np.sqrt(np.diag(pcov2))
print("Gli errori sono: ", exa2, exb2)
print("Il fattore di cov(A,B) è", pcov2[0][1], "Mentre quello di cov(B,A) è", pcov2[1][0])

print("")
tstar2 = (-xa+xa2)/(-xb2+xb)
print("Ricalcolando t* con questo nuovo metodo otteniamo: ", tstar2)
print("Da cui ricaviamo g:", 4*np.pi**2*0.994/(tstar2**2))

etstar2 = ((-xa+xa2)/(-xb2+xb)**2)**2*(exa**2+exa2**2)
etstar2 = etstar2 + (1/(-xb2+xb))**2*(exb**2+exb2**2)
etstar2 = etstar2 + 2*((-xa+xa2)/(-xb2+xb)**3)*(pcov[0][1]+pcov[0][1])
print("L'errore su t*2 è", etstar2)


plt.plot(intervalli, lrossa, color='#0096c7')
plt.plot(intervalli, lblue, color='#f07167')
plt.errorbar(tstar[0], tstar[1], marker='*', label="t*", color='k', xerr=0.2, yerr=etstar)
plt.errorbar(intervalli[:2:], meds[:4:2], xerr=0.2, yerr=0.00001, fmt='o', label='Peso aggiuntivo sul basso')
plt.errorbar(intervalli[:2:], meds[1:4:2], xerr=0.2, yerr=0.00001, fmt='o', color='red', label='Peso aggiuntivo in alto')
plt.xlim(34.8, 36.5)
plt.legend(loc='lower left')
plt.xlabel("Distanza massa mobile (cm)")
plt.ylabel("Tempi di oscillazione (s)")
plt.show()
