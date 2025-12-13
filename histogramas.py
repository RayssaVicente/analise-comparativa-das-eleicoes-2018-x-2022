import glob
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

# --- configurações ---
pasta_2018 = "votacao_partido_munzona_2018"
pasta_2022 = "votacao_partido_munzona_2022"

# Colunas esperadas (se suas colunas tiverem nomes diferentes,
# o script tenta achar variações contendo essas strings)
PARTY_KEYWORDS = ["SG_PARTIDO", "PARTIDO", "SIGLA"]
VOTES_KEYWORDS = ["QT_VOTOS_NOMINAIS_VALIDOS", "QT_VOTOS", "VOTOS_NOMINAIS", "VOTOS"]
COLIG_KEYWORDS = ["NM_COLIGACAO", "COLIGACAO", "NM_COLIGA"]

# Funções utilitárias
def find_column_name(header, keywords):
    # header: Index de colunas lidas (originais)
    header_upper = [c.strip().upper() for c in header]
    for kw in keywords:
        for i, col in enumerate(header_upper):
            if kw.upper() in col:
                return header[i]  # devolve nome real da coluna
    return None

def read_and_aggregate(pattern, party_kw=PARTY_KEYWORDS, votes_kw=VOTES_KEYWORDS, colig_kw=COLIG_KEYWORDS, use_colig=False):
    files = glob.glob(os.path.join(pattern, "*.csv"))
    if not files:
        print(f"[ERRO] Nenhum arquivo encontrado em: {pattern}")
        return pd.Series(dtype=int), (pd.Series(dtype=int) if use_colig else None)

    party_totals = Counter()
    colig_totals = Counter() if use_colig else None

    # Detecta colunas a partir do primeiro arquivo (tenta ';' e fallback)
    # Usamos nrows=0 para só ler o header e economizar I/O.
    first = files[0]
    try:
        header = pd.read_csv(first, sep=';', encoding='latin1', nrows=0).columns
    except Exception:
        header = pd.read_csv(first, nrows=0).columns

    party_col = find_column_name(header, party_kw)
    votes_col = find_column_name(header, votes_kw)
    colig_col = find_column_name(header, colig_kw) if use_colig else None

    if party_col is None or votes_col is None:
        print("[ERRO] Não encontrei automaticamente as colunas de partido ou votos.")
        print("Colunas encontradas no primeiro arquivo:", list(header))
        raise KeyError("Ajuste PARTY_KEYWORDS / VOTES_KEYWORDS ou verifique os nomes das colunas nos CSVs.")

    print(f"[INFO] Usando colunas: partido='{party_col}' votos='{votes_col}' coligação='{colig_col}'")

    for fpath in files:
        try:
            # lê apenas as colunas necessárias como strings (evita conversão automática pesada)
            usecols = [party_col, votes_col] + ([colig_col] if use_colig and colig_col else [])
            df = pd.read_csv(fpath, sep=';', encoding='latin1', usecols=usecols, dtype=str, low_memory=True)
        except Exception as e:
            # fallback: tenta ler sem sep fixo (caso variem)
            df = pd.read_csv(fpath, dtype=str, low_memory=True)

        # normaliza colunas (remove espaços)
        df.columns = df.columns.str.strip()

        # limpa e converte votos para inteiro (remove separador de milhares)
        s_votes = df[votes_col].astype(str).str.replace('.', '', regex=False).str.replace(',', '', regex=False)
        s_votes = pd.to_numeric(s_votes, errors='coerce').fillna(0).astype(int)

        df[votes_col] = s_votes
        df[party_col] = df[party_col].astype(str).str.strip()

        # agrega por partido no arquivo atual e atualiza contador
        group_party = df.groupby(party_col)[votes_col].sum()
        for party, val in group_party.items():
            party_totals[str(party)] += int(val)

        # se quiser coligação também (somente para 2022)
        if use_colig and colig_col and colig_col in df.columns:
            df[colig_col] = df[colig_col].astype(str).str.strip()
            group_colig = df.groupby(colig_col)[votes_col].sum()
            for colig, val in group_colig.items():
                colig_totals[str(colig)] += int(val)

    # transforma em Series pandas ordenada
    s_party = pd.Series(dict(party_totals)).sort_values(ascending=False)
    s_colig = pd.Series(dict(colig_totals)).sort_values(ascending=False) if use_colig else None
    return s_party, s_colig

# --- execução ---
votos_2018, _ = read_and_aggregate(pasta_2018, use_colig=False)
votos_2022, votos_colig_2022 = read_and_aggregate(pasta_2022, use_colig=True)

print("Partidos 2018 lidos:", len(votos_2018))
print("Partidos 2022 lidos:", len(votos_2022))
if votos_colig_2022 is not None:
    print("Coligações 2022 lidas:", len(votos_colig_2022))

# --- plota (função simples) ---
def plot_top_series(series, title, max_items=80, horizontal=True, save_as=None):
    if series is None or series.empty:
        print("[WARN] Série vazia, nada a plotar:", title)
        return
    if len(series) > max_items:
        top = series.head(max_items)
        others = series.iloc[max_items:].sum()
        top["OUTROS"] = others
        s = top
        print(f"[INFO] Mais de {max_items} categorias — exibindo top {max_items} + OUTROS.")
    else:
        s = series

    plt.figure(figsize=(12, max(4, 0.25 * len(s))))
    if horizontal:
        plt.barh(s.index[::-1], s.values[::-1])  # maior embaixo
        plt.xlabel("Número de votos")
    else:
        plt.bar(s.index, s.values)
        plt.xticks(rotation=90)
        plt.ylabel("Número de votos")
    plt.title(title)
    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, bbox_inches='tight')
        print("[INFO] Salvo em:", save_as)
    plt.show()

plot_top_series(votos_2018, "Total de votos por partido – Eleições 2018", max_items=120, horizontal=True, save_as="votos_2018.png")
plot_top_series(votos_2022, "Total de votos por partido – Eleições 2022", max_items=120, horizontal=True, save_as="votos_2022.png")
if votos_colig_2022 is not None:
    plot_top_series(votos_colig_2022, "Total de votos por coligação – Eleições 2022", max_items=120, horizontal=True, save_as="votos_colig_2022.png")

# --- variação percentual ---
df_var = pd.DataFrame({"votos_2018": votos_2018, "votos_2022": votos_2022}).fillna(0)
df_var = df_var[df_var["votos_2018"] > 0]
df_var["var_percent"] = (df_var["votos_2022"] - df_var["votos_2018"]) / df_var["votos_2018"] * 100
plot_top_series(df_var["var_percent"].sort_values(ascending=True), "Variação percentual 2018 x 2022 (%)", max_items=120, horizontal=True, save_as="variacao_percentual.png")
