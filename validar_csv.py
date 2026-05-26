import pandas as pd

df = pd.read_csv("data/documentos.csv", sep=";")

print(df.head())
print()
print("Colunas originais:", list(df.columns))
print("Quantidade de documentos:", len(df))

assert list(df.columns) == ["id", "documento"], "As colunas precisam ser exatamente id e documento"
assert len(df) >= 35, "Precisa ter pelo menos 35 documentos"
assert df["id"].is_unique, "Os IDs precisam ser únicos"
assert df["documento"].notna().all(), "Não pode ter documento vazio"

df["tokens"] = df["documento"].astype(str).apply(lambda x: len(x.split()))

print()
print("Maiores documentos:")
print(df[["id", "tokens"]].sort_values("tokens", ascending=False).head())

assert (df["tokens"] <= 350).all(), "Tem documento com mais de 350 tokens"

print()
print("Tudo certo com o documentos.csv!")