import pandas as pd
from gensim.models import Word2Vec, FastText
import numpy as np

w2v = Word2Vec.load("embeddings/word2vec.model")
ft = FastText.load("embeddings/fasttext.model")

seed_words = ["yaxşı", "pis", "çox", "bahalı", "ucuz", "mükəmməl", "dəhşət", "<PRICE>", "<RATING_POS>"]
syn_pairs = [("yaxşı", "əla"), ("bahalı", "qiymətli"), ("ucuz", "sərfəli")]
ant_pairs = [("yaxşı", "pis"), ("bahalı", "ucuz")]

def lexical_coverage(model, tokens):
    vocab = model.wv.key_to_index
    return sum(1 for t in tokens if t in vocab) / max(1, len(tokens))

def read_tokens(f):
    df = pd.read_excel(f, usecols=["cleaned_text"])
    return [t for row in df["cleaned_text"].astype(str) for t in row.split()]

files = [
    "labeled-sentiment_2col.xlsx",
    "test__1__2col.xlsx",
    "train__3__2col.xlsx",
    "train-00000-of-00001_2col.xlsx",
    "merged_dataset_CSV__1__2col.xlsx",
]

print("== Lexical Coverage ==")
for f in files:
    toks = read_tokens(f)
    cov_w2v = lexical_coverage(w2v, toks)
    cov_ft = lexical_coverage(ft, toks)
    print(f"{f}: W2V={cov_w2v:.3f}, FastText={cov_ft:.3f}")

def pair_sim(model, pairs):
    vals = []
    for a, b in pairs:
        try:
            vals.append(model.wv.similarity(a, b))
        except KeyError:
            pass
    return np.mean(vals) if vals else np.nan

syn_w2v, syn_ft = pair_sim(w2v, syn_pairs), pair_sim(ft, syn_pairs)
ant_w2v, ant_ft = pair_sim(w2v, ant_pairs), pair_sim(ft, ant_pairs)

print("\n== Synonym/Antonym Similarities ==")
print(f"Synonyms:  W2V={syn_w2v:.3f}, FastText={syn_ft:.3f}")
print(f"Antonyms:  W2V={ant_w2v:.3f}, FastText={ant_ft:.3f}")
print(f"Separation (Syn-Ant): W2V={syn_w2v - ant_w2v:.3f}, FastText={syn_ft - ant_ft:.3f}")

def neighbors(model, word, k=5):
    try:
        return [w for w, _ in model.wv.most_similar(word, topn=k)]
    except KeyError:
        return []

print("\n== Nearest Neighbors ==")
for w in seed_words:
    print(f"W2V '{w}':", neighbors(w2v, w))
    print(f"FT  '{w}':", neighbors(ft, w))
