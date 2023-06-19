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


def histog(arr, orient, nome):
    nbins = int(np.ceil(np.log2(len(arr)))) + 1   # Scegliamo il numero di bins con la regola di Stourges

    if orient == 1:
        colors = 'red'
    else:
        colors = 'blue'

    plt.hist(arr, bins=nbins, color=colors)
    plt.title("Distanza " + nome[5:7:] + " cm " + "configurazione " + nome[11:12:])
    plt.show()
    print("Distanza (cm): " + nome[5:7:])
    media_varianza_min_max(arr)


def apri(nome, orient):
    df = pd.read_csv(nome, on_bad_lines='skip')
    colonna = df['Ultimo']
    histog(colonna, orient, nome)
    return colonna

global listmedie

apri("venv/35conf1.csv", 1)
apri("venv/35conf2.csv", 2)
apri("venv/36conf1.csv", 1)
apri("venv/36conf2.csv", 2)
apri("venv/37conf1.csv", 1)
apri("venv/37conf2.csv", 2)
apri("venv/39conf1.csv", 1)
apri("venv/39conf2.csv", 2)
