import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd


def media_varianza_min_max(arr):
    print("La media è:", np.mean(arr))
    print("La varianza è:", np.var(arr))
    print("La stdev è:", np.std(arr))
    print("Il massimo ed il minimo valore registrati sono:", max(arr), min(arr))


def histog(arr):
    nbins = np.log2(len(arr)) + 1   # Scegliamo il numero di bins con la regola di Stourges
    plt.hist(arr, bins=nbins, color='green')
    media_varianza_min_max(arr)


def apri(nome):
    df = pd.read_csv(nome, on_bad_lines='skip')
    colonna = df['Ultimo']
    print(colonna)
    return colonna


columns = apri("venv/35 configurazione 1.csv")
media_varianza_min_max(columns)
