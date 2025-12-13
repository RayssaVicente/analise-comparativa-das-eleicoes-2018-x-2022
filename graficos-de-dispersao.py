import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

arquivos_2018 = glob.glob("votacao_partido_munzona_2018/*.csv")
arquivos_2022 = glob.glob("votacao_partido_munzona_2022/*.csv")

df2018 = pd.concat([pd.read_csv(arq, sep=";", encoding="latin1") for arq in arquivos_2018], ignore_index=True)
df2022 = pd.concat([pd.read_csv(arq, sep=";", encoding="latin1") for arq in arquivos_2022], ignore_index=True)

# Agrupa por partido
votos_partido_2018 = df2018.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS_VALIDOS"].sum()
votos_partido_2022 = df2022.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS_VALIDOS"].sum()

# Junta em um DataFrame
df_variacao = pd.DataFrame({
    "votos_2018": votos_partido_2018,
    "votos_2022": votos_partido_2022
}).fillna(0)

df_variacao = df_variacao[df_variacao["votos_2018"] > 0]

df_variacao["var_percentual"] = (
    (df_variacao["votos_2022"] - df_variacao["votos_2018"]) / df_variacao["votos_2018"] * 100
)

# Cria subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Função para adicionar rótulos (partidos) em cada ponto com espaçamento
def add_labels(ax, x, y, labels, dx=0.02, dy=0.02):
    for i, label in enumerate(labels):
        ax.text(x[i] + dx, y[i] + dy, label, fontsize=8, alpha=0.7)

# 1 - Dispersão: votos 2018 x votos 2022
axs[0,0].scatter(df_variacao["votos_2018"], df_variacao["votos_2022"], alpha=0.7)
add_labels(axs[0,0], df_variacao["votos_2018"], df_variacao["votos_2022"], df_variacao.index)
axs[0,0].set_title("Votos 2018 x Votos 2022")
axs[0,0].set_xlabel("Votos 2018")
axs[0,0].set_ylabel("Votos 2022")

# 2 - Dispersão: votos 2018 x variação %
axs[0,1].scatter(df_variacao["votos_2018"], df_variacao["var_percentual"], alpha=0.7, color="orange")
add_labels(axs[0,1], df_variacao["votos_2018"], df_variacao["var_percentual"], df_variacao.index)
axs[0,1].set_title("Votos 2018 x Variação %")
axs[0,1].set_xlabel("Votos 2018")
axs[0,1].set_ylabel("Variação %")

# 3 - Dispersão: votos 2022 x variação %
axs[1,0].scatter(df_variacao["votos_2022"], df_variacao["var_percentual"], alpha=0.7, color="green")
add_labels(axs[1,0], df_variacao["votos_2022"], df_variacao["var_percentual"], df_variacao.index)
axs[1,0].set_title("Votos 2022 x Variação %")
axs[1,0].set_xlabel("Votos 2022")
axs[1,0].set_ylabel("Variação %")

# 4 - Dispersão normalizado
df_variacao["votos_2018_norm"] = df_variacao["votos_2018"] / df_variacao["votos_2018"].max()
df_variacao["votos_2022_norm"] = df_variacao["votos_2022"] / df_variacao["votos_2022"].max()
axs[1,1].scatter(df_variacao["votos_2018_norm"], df_variacao["votos_2022_norm"], alpha=0.7, color="red")
add_labels(axs[1,1], df_variacao["votos_2018_norm"], df_variacao["votos_2022_norm"], df_variacao.index)
axs[1,1].set_title("Normalizado: Votos 2018 x Votos 2022")
axs[1,1].set_xlabel("Votos 2018 (escala 0-1)")
axs[1,1].set_ylabel("Votos 2022 (escala 0-1)")

plt.tight_layout()
plt.show()
