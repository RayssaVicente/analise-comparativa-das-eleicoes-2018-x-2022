import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np


arquivos_2018 = glob.glob("votacao_partido_munzona_2018/*.csv")
arquivos_2022 = glob.glob("votacao_partido_munzona_2022/*.csv")

df2018 = pd.concat([pd.read_csv(arq, sep=";", encoding="latin1") for arq in arquivos_2018], ignore_index=True)
df2022 = pd.concat([pd.read_csv(arq, sep=";", encoding="latin1") for arq in arquivos_2022], ignore_index=True)

#  Agrupa por partido (2018 e 2022) 
votos_partido_2018 = df2018.groupby("SG_PARTIDO")["QT_TOTAL_VOTOS_LEG_VALIDOS"].sum()
votos_partido_2022 = df2022.groupby("SG_PARTIDO")["QT_TOTAL_VOTOS_LEG_VALIDOS"].sum()

#  Junta em um DataFrame para calcular variação 
df_variacao = pd.DataFrame({
    "votos_2018": votos_partido_2018,
    "votos_2022": votos_partido_2022
}).fillna(0)

# Evita divisão por zero
df_variacao = df_variacao[df_variacao["votos_2018"] > 0]

# passo 1 Calcula a variação percentual
df_variacao["var_percentual"] = (
    (df_variacao["votos_2022"] - df_variacao["votos_2018"]) / df_variacao["votos_2018"] * 100
)

# passo 2 Filtra valores válidos
valores_validos = df_variacao["var_percentual"].replace([np.inf, -np.inf], np.nan).dropna()

def resumo_estatistico(serie, nome):
    media = np.mean(serie)
    mediana = np.median(serie)
    desvio = np.std(serie)

    print(f"{nome}")
    print(f"   Média   : {media:,.2f}")
    print(f"   Mediana : {mediana:,.2f}")
    print(f"   Desvio Padrão : {desvio:,.2f}")
    print("-"*50)


#  Estatísticas descritivas 
resumo_estatistico(votos_partido_2018, "Votos por partido – 2018")
resumo_estatistico(votos_partido_2022, "Votos por partido – 2022")
resumo_estatistico(valores_validos, "Variação percentual 2018 → 2022")

