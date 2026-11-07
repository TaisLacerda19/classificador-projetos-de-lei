"""Preparo de texto compartilhado entre a análise e o classificador."""

from sklearn.feature_extraction.text import TfidfVectorizer

PALAVRAS_VAZIAS = sorted(set("""
a o e de da do das dos em no na nos nas para por com que se ao aos as os um uma sobre
lei n dispoe altera institui da outras providencias
""".split()))


def limpar(ementa):
    """Remove o marcador de ementa alterada, que não diz nada sobre o tema."""
    return ementa.replace('NOVA EMENTA:', ' ')


def criar_vetorizador():
    return TfidfVectorizer(
        strip_accents='unicode',
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True,
        stop_words=PALAVRAS_VAZIAS,
    )
