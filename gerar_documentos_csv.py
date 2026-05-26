from pathlib import Path
import csv
import re

PASTA_CSTNEWS = Path(r"C:\Users\Cleit\Downloads\CSTNews 6.0\CSTNews 6.0")

SAIDA = Path("data/documentos.csv")

def limpar_texto(texto: str) -> str:
    texto = texto.replace("\ufeff", "")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def ler_arquivo_texto(caminho: Path) -> str | None:
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return caminho.read_text(encoding=encoding)
        except UnicodeDecodeError:
            pass
    return None

documentos = []

pastas_textos_fonte = list(PASTA_CSTNEWS.rglob("Textos-fonte"))

print(f"Pastas Textos-fonte encontradas: {len(pastas_textos_fonte)}")

for pasta in sorted(pastas_textos_fonte):
    arquivos_txt = sorted(pasta.rglob("*.txt"))

    for arquivo in arquivos_txt:
        texto = ler_arquivo_texto(arquivo)

        if texto is None:
            print(f"Não consegui ler: {arquivo}")
            continue

        texto = limpar_texto(texto)

        if not texto:
            continue

        tokens = texto.split()

        if len(tokens) > 350:
            texto = " ".join(tokens[:500])

        documentos.append(texto)

        print(f"{len(documentos):02d} - {arquivo}")

        if len(documentos) >= 40:
            break

    if len(documentos) >= 40:
        break

SAIDA.parent.mkdir(exist_ok=True)

with SAIDA.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["id", "documento"])

    for i, documento in enumerate(documentos, start=1):
        writer.writerow([i, documento])

print()
print(f"Arquivo gerado: {SAIDA}")
print(f"Quantidade de documentos: {len(documentos)}")

if len(documentos) < 30:
    print("ATENÇÃO: foram encontrados menos de 30 documentos.")