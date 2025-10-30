# 🧠 CENG 442 – Assignment 1

### Azerbaijani Text Preprocessing + Word Embeddings (Domain-Aware)

---

## 1️⃣ Data & Goal

Five Azerbaijani sentiment-analysis datasets were cleaned and relabeled using three sentiment levels
(**Negative = 0.0**, **Neutral = 0.5**, **Positive = 1.0**).
Each dataset was converted into a two-column Excel file (`cleaned_text`, `sentiment_value`), then merged into a single corpus (`corpus_all.txt`).
The goal is to train **Word2Vec** and **FastText** embeddings and compare their performance across domains (news, social, reviews, general).

---

## 2️⃣ Preprocessing (Rules Summary)

All cleaning and normalization were performed automatically using `main.py`.
Key rules:

* Azerbaijani-specific lower-casing (`İ→i`, `I→ı`), Unicode NFC normalization.
* Replace URLs → `URL`, emails → `EMAIL`, phones → `PHONE`, @mentions → `USER`.
* Hashtag split: `#QarabagIsBack → qarabag is back`.
* Emoji mapping 🙂→`EMO_POS`, ☹→`EMO_NEG`.
* Numbers → `<NUM>`; collapse ≥ 3 repeated letters → 2 (`cooool → coool`).
* Negation scope: mark next 3 tokens with `_NEG` after negators (`yox`, `deyil`, etc.).
* Domain detection + `dom<domain>` prefix per line.
* Remove duplicates and empty rows.

**Result:** ≈ 124 k sentences in `corpus_all.txt`.

---

## 3️⃣ Mini Challenges (Implemented)

* ✅ Hashtag splitting (`#QarabagIsBack → qarabag is back`)
* ✅ Emoji mapping 🙂/☹ → EMO_POS / EMO_NEG
* ✅ Negation scope annotation (`yaxşı deyil → yaxşı_NEG`)
* ✅ Stopword research (AZ–TR comparison; 20 candidate stopwords)
* ✅ De-asciification (`cox → çox`, `yaxsi → yaxşı`)

---

## 4️⃣ Domain-Aware Processing

Domains were detected using lightweight regex rules and tagged in the corpus.

| Domain  | Trigger Patterns                        |
| :------ | :-------------------------------------- |
| news    | apa, trend, azertac, reuters, bloomberg |
| social  | @, #, 😂, 😍, 🙂                        |
| reviews | azn, manat, qiymət, ulduz               |
| general | default case                            |

**Examples**

```
domreviews  çox yaxşı məhsuldur
domsocial   😂 bu gün çox gözəl idi
```

---

## 5️⃣ Embeddings – Training & Results

### Training Settings

| Parameter     | Value              |
| :------------ | :----------------- |
| vector_size   | 300                |
| window        | 5                  |
| min_count     | 3                  |
| sg            | 1 (Skip-Gram)      |
| epochs        | 10                 |
| negative      | 10 (Word2Vec only) |
| min_n / max_n | 3 / 6 (FastText)   |

---

### Lexical Coverage

| Dataset              | Word2Vec | FastText |
| :------------------- | :------: | :------: |
| labeled-sentiment    |   0.932  |   0.932  |
| test__1_             |   0.987  |   0.987  |
| train__3_            |   0.990  |   0.990  |
| train-00000-of-00001 |   0.943  |   0.943  |
| merged_dataset       |   0.949  |   0.949  |

---

### Synonym / Antonym Similarities

| Metric                 | Word2Vec | FastText |
| :--------------------- | :------: | :------: |
| Synonyms               |   0.355  |   0.445  |
| Antonyms               |   0.347  |   0.429  |
| Separation (Syn – Ant) |   0.008  |   0.016  |

---

### Nearest Neighbors (Examples)

```
'yaxşı' → W2V: ['<RATING_POS>', 'yaxshi', 'yaxsi']
'yaxşı' → FT: ['yaxşıl', 'yaxşılıq', 'yaxşıca']
'ucuz'  → ['ucuzdur', 'ucuzluğa', 'ucuza']
'mükəmməl' → ['möh­təşəm', 'mükəmməldi', 'mükəmmal']
```

---

## 6️⃣ Reproducibility

| Component | Version    |
| :-------- | :--------- |
| Python    | 3.11.9     |
| pandas    | 2.3        |
| gensim    | 4.4        |
| numpy     | 1.26       |
| OS        | Windows 11 |

**Run sequence:**

```bash
python main.py
python train_embeddings.py
python compare_models.py
```

---

## 7️⃣ Conclusions

* **FastText** outperforms on morphologically rich forms (e.g., *yaxsi ↔ yaxşı*) due to subword modeling.
* **Word2Vec** is more stable for frequent tokens but fails for OOV words.
* Overall coverage 93 – 99 % → excellent tokenization and corpus consistency.
* Future work: domain-specific training (e.g., `domnews` vs `domsocial`) and cross-domain drift analysis.

---

## 👥 Group Members

* Efe Şahin
* Selin Sargın

---

## 📦 Repository Structure

```
main.py
train_embeddings.py
compare_models.py
requirements.txt
labeled-sentiment_2col.xlsx
test__1__2col.xlsx
train__3__2col.xlsx
train-00000-of-00001_2col.xlsx
merged_dataset_CSV__1__2col.xlsx
corpus_all.txt
```

**Embeddings (Google Drive):**
[https://drive.google.com/drive/folders/](https://drive.google.com/drive/folders/)<YOUR_DRIVE_LINK_HERE>
