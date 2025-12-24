# 📊 Análise Comparativa da Votação Partidária – Eleições 2018 x 2022 (TSE)

## 📌 Descrição do Projeto
Este projeto realiza uma **análise comparativa da votação nominal por partido** nas eleições brasileiras de **2018 e 2022**, utilizando **dados públicos do Tribunal Superior Eleitoral (TSE)**.

O objetivo é identificar **padrões, tendências e variações no desempenho eleitoral dos partidos políticos** entre os dois pleitos, por meio de **análise exploratória de dados (EDA)** e **visualizações gráficas**.

---

## 🎯 Objetivos da Análise
- Comparar o total de votos nominais por partido entre 2018 e 2022  
- Identificar crescimento ou queda percentual de votos por partido  
- Avaliar a relação entre desempenho eleitoral passado e atual  
- Visualizar tendências por meio de gráficos de dispersão  
- Normalizar os dados para comparação entre partidos de diferentes tamanhos  

---

## 🧠 Tecnologias Utilizadas
- **Python**
- **Pandas** — manipulação e análise de dados  
- **Matplotlib** — visualização de dados  
- **NumPy** — operações numéricas  
- **Glob** — leitura de múltiplos arquivos CSV  
- **Dados públicos do TSE**

---

## 📂 Estrutura do Projeto
analise-votacao-tse/
│
├── votacao_partido_munzona_2018/
│ └── arquivos CSV (TSE - 2018)
│
├── votacao_partido_munzona_2022/
│ └── arquivos CSV (TSE - 2022)
│
├── graficos-de-dispersao.py
└── README.md


---

## 🔎 Metodologia
1. **Coleta dos dados**: Leitura de múltiplos arquivos CSV do TSE para os anos de 2018 e 2022  
2. **Tratamento dos dados**:
   - Padronização de encoding (`latin1`)
   - Consolidação dos arquivos em DataFrames únicos  
3. **Agregação**:
   - Soma dos votos nominais válidos por partido  
4. **Criação de métricas**:
   - Variação percentual de votos entre os anos  
5. **Análise exploratória**:
   - Comparações diretas
   - Normalização dos dados  
6. **Visualização**:
   - Gráficos de dispersão com identificação dos partidos  

---

## 📈 Visualizações Geradas
O script gera quatro gráficos principais:

1. **Dispersão: Votos 2018 x Votos 2022**  
   → Avalia a correlação entre o desempenho eleitoral nos dois pleitos  

2. **Dispersão: Votos 2018 x Variação Percentual**  
   → Identifica partidos com crescimento ou queda proporcional relevante  

3. **Dispersão: Votos 2022 x Variação Percentual**  
   → Analisa o impacto do desempenho atual na variação percentual  

4. **Dispersão Normalizada (0–1)**  
   → Permite comparar partidos de diferentes tamanhos em escala comum  

---

## 💡 Principais Insights
- Partidos com maior base eleitoral em 2018 tendem a manter vantagem em 2022  
- Alguns partidos apresentaram **crescimento percentual expressivo**, mesmo partindo de bases menores  
- A normalização dos dados permite uma análise mais justa entre partidos grandes e pequenos  

## ▶️ Como Executar o Projeto
1. Organize os arquivos CSV do TSE nas pastas correspondentes (`2018` e `2022`)
2. Instale as dependências:
```bash
pip install pandas matplotlib numpy

## Desenvolvido por Rayssa Vicente
