"""Indica os temas mais prováveis de uma ementa.

Uso: python classificar.py "Dispõe sobre a vacinação gratuita em escolas públicas."
"""

import sys

import pandas as pd
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import make_pipeline

from modelo import criar_vetorizador, limpar


def treinar():
    projetos = pd.read_csv('dados/projetos_de_lei.csv').drop_duplicates('ementa')
    modelo = make_pipeline(criar_vetorizador(), ComplementNB())
    return modelo.fit(projetos['ementa'].map(limpar), projetos['tema'])


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python classificar.py "texto da ementa"')
    modelo = treinar()
    probabilidades = modelo.predict_proba([limpar(sys.argv[1])])[0]
    ranking = sorted(zip(modelo.classes_, probabilidades), key=lambda item: item[1], reverse=True)
    for tema, probabilidade in ranking[:3]:
        print(f'{tema}: {probabilidade:.0%}')


if __name__ == '__main__':
    main()
