"""Baixa as ementas de projetos de lei da Câmara dos Deputados por tema."""

import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

URL = (
    'https://dadosabertos.camara.leg.br/api/v2/proposicoes'
    '?siglaTipo=PL&ano={ano}&codTema={tema}&itens=100&pagina={pagina}&ordem=ASC&ordenarPor=id'
)
ANOS = (2023, 2024)
TEMAS = {
    40: 'Economia',
    43: 'Direito Penal',
    46: 'Educação',
    48: 'Meio Ambiente',
    56: 'Saúde',
    58: 'Trabalho e Emprego',
    61: 'Transporte',
    67: 'Defesa do Consumidor',
}


def baixar_pagina(ano, tema, pagina):
    url = URL.format(ano=ano, tema=tema, pagina=pagina)
    pedido = Request(url, headers={'User-Agent': 'portfolio-dados', 'Accept': 'application/json'})
    with urlopen(pedido, timeout=60) as resposta:
        return json.load(resposta)['dados']


def baixar_tema(ano, tema):
    linhas = []
    pagina = 1
    while True:
        dados = baixar_pagina(ano, tema, pagina)
        linhas.extend(dados)
        if len(dados) < 100:
            return linhas
        pagina += 1
        time.sleep(0.2)


def main():
    linhas = []
    for ano in ANOS:
        for codigo, nome in TEMAS.items():
            registros = baixar_tema(ano, codigo)
            print(f'{ano} {nome}: {len(registros)}')
            linhas.extend(
                {'id': r['id'], 'numero': r['numero'], 'ano': r['ano'], 'ementa': r['ementa'], 'tema': nome}
                for r in registros
            )

    tabela = pd.DataFrame(linhas)
    temas_por_projeto = tabela.groupby('id')['tema'].transform('nunique')
    unicos = tabela[temas_por_projeto == 1].drop_duplicates('id').sort_values('id')

    Path('dados').mkdir(exist_ok=True)
    unicos.to_csv('dados/projetos_de_lei.csv', index=False)
    print(f'{tabela["id"].nunique()} projetos no total, {len(unicos)} com um único tema entre os escolhidos')


if __name__ == '__main__':
    main()
