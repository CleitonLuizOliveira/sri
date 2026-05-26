import ast
import pandas as pd
import spacy
from pathlib import Path

DATA_DIR = Path("data")
ARQUIVO_DATASET = DATA_DIR / "dataset.csv"
ARQUIVO_SAIDA = DATA_DIR / "datasetner.csv"

print("Carregando dataset.csv...")
df_dataset = pd.read_csv(ARQUIVO_DATASET, sep=";", encoding="UTF-8")

print("Convertendo sentenças...")
df_dataset["sentencas"] = df_dataset["sentencas"].apply(
    lambda x: ast.literal_eval(x) if type(x) != list else x
)

print("Carregando spaCy...")
try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    print("Modelo pt_core_news_lg não encontrado. Tentando pt_core_news_sm...")
    nlp = spacy.load("pt_core_news_sm")

dataset_ner = []

print(f"Processando {len(df_dataset)} documentos...")

for _, linha in df_dataset.iterrows():
    id_documento = linha["id"]
    sentencas = linha["sentencas"]

    ner_documento = []

    for indice_sentenca, sentenca in enumerate(sentencas):
        doc = nlp(str(sentenca))

        entidades = []

        for ent in doc.ents:
            entidades.append([
                ent.text,
                ent.label_,
                ent.start_char,
                ent.end_char
            ])

        ner_documento.append([
            indice_sentenca,
            entidades
        ])

    dataset_ner.append([
        id_documento,
        ner_documento
    ])

df_ner = pd.DataFrame(dataset_ner, columns=["id", "ner_documento"])
df_ner.to_csv(ARQUIVO_SAIDA, sep=";", index=False, encoding="UTF-8")

print("Pronto!")
print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
print(f"Total de documentos NER: {len(df_ner)}")
print(df_ner.head())