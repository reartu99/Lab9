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


def tstarcalc(T11, T12, T22, T21, et):
    tstar = ((T11*T22)-(T12*T21))/((T22*T21)-(T12*T11))
    errtstar = 0
    return tstar, errtstar


def linee(ranges, T11, T12, T22, T21, x1, x2):
    linearossa = []
    lineablue = []
    for x in ranges:
        linearossa.append(((T21-T11)/(x2-x1))*(x-x1)+T11)
    for x in ranges:
        lineablue.append(((T22-T12)/(x2-x1))*(x-x1)+T12)
    return linearossa, lineablue

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

plt.errorbar(intervalli, meds[::2], xerr=0.1, fmt='o')
plt.errorbar(intervalli, meds[1::2], xerr=0.1, fmt='o', color='red')
lrossa, lblue = linee(intervalli, meds[0], meds[1], meds[3], meds[4], 35, 36)
plt.plot(lrossa)
plt.plot(lblue)
plt.show()
print("T* sarebbe:" + str(tstarcalc(meds[0], meds[1], meds[3], meds[4], 1)))
