
import pandas as pd

# ==========================================
# QUESTÃO 1 - EXPLORAÇÃO INICIAL
# ==========================================

# 1. Carregando o arquivo CSV
df = pd.read_csv("investimentos.csv", sep=";", encoding="utf-8")

# 2. Convertendo a coluna de data para o formato correto
df["data_referencia"] = pd.to_datetime(
    df["data_referencia"], errors="coerce"
)

# 3. Quantidade de registros e colunas
print("\n===== EXPLORAÇÃO INICIAL =====")

print("\nQuantidade de registros:")
print(df.shape[0])

print("\nQuantidade de colunas:")
print(df.shape[1])

# 4. Listando os nomes das colunas
print("\nNomes das colunas:")
print(df.columns.tolist())

# 5. Verificando os tipos de dados
print("\nTipos de dados:")
print(df.dtypes)

# 6. Verificando informações gerais
print("\nInformações gerais:")
df.info()

# 7. Verificando valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())

# 8. Verificando registros duplicados
print("\nRegistros duplicados:")
print(df.duplicated().sum())

# 9. Verificando datas inválidas
print("\nDatas inválidas:")
print(df["data_referencia"].isnull().sum())

# 10. Visualizando os primeiros registros
print("\nPrimeiros registros:")
print(df.head())

# ==========================================
# QUESTÃO 2 - QUALIDADE E TRATAMENTO DOS DADOS
# ==========================================

print("\n===== QUALIDADE E TRATAMENTO DOS DADOS =====")

# 1. Separando os registros de moedas e indicadores
dados_moedas = df[df["moeda"].notna()].copy()
dados_indicadores = df[df["indicador_economico"].notna()].copy()

print("\nQuantidade de registros de moedas:")
print(len(dados_moedas))

print("\nQuantidade de registros de indicadores:")
print(len(dados_indicadores))


# 2. Verificando valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())


# 3. Verificando registros duplicados
print("\nQuantidade de registros duplicados:")
print(df.duplicated().sum())

print("\nQuantidade de IDs duplicados:")
print(df["id_registro"].duplicated().sum())


# 4. Verificando valores inválidos nas cotações
print("\n===== VERIFICAÇÃO DAS COTAÇÕES =====")

print("\nCotações de compra menores ou iguais a zero:")
print((dados_moedas["cotacao_compra"] <= 0).sum())

print("\nCotações de venda menores ou iguais a zero:")
print((dados_moedas["cotacao_venda"] <= 0).sum())

print("\nCotações de compra maiores que as de venda:")
print((dados_moedas["cotacao_compra"] >
       dados_moedas["cotacao_venda"]).sum())


# 5. Conferindo a cotação média
media_calculada = (
    dados_moedas["cotacao_compra"] +
    dados_moedas["cotacao_venda"]
) / 2

diferencas = (
    dados_moedas["cotacao_media"] - media_calculada
).abs()

print("\nCotações médias fora da margem de arredondamento:")
print((diferencas > 0.0001).sum())


# 6. Identificando valores estatisticamente atípicos
print("\n===== VALORES ATÍPICOS POR MOEDA =====")

for moeda, grupo in dados_moedas.groupby("codigo_moeda"):

    q1 = grupo["cotacao_media"].quantile(0.25)
    q3 = grupo["cotacao_media"].quantile(0.75)

    intervalo = q3 - q1

    limite_inferior = q1 - 1.5 * intervalo
    limite_superior = q3 + 1.5 * intervalo

    atipicos = grupo[
        (grupo["cotacao_media"] < limite_inferior) |
        (grupo["cotacao_media"] > limite_superior)
    ]

    print(f"{moeda}: {len(atipicos)} valores atípicos")


# 7. Verificando indicadores econômicos negativos
print("\nIndicadores econômicos negativos:")

print(
    dados_indicadores[
        dados_indicadores["valor_indicador"] < 0
    ][["indicador_economico", "valor_indicador"]]
)


# 8. Conferindo o resultado final
print("\n===== RESUMO DA VERIFICAÇÃO =====")

print("Total de registros:", len(df))
print("Total de registros de moedas:", len(dados_moedas))
print("Total de registros de indicadores:", len(dados_indicadores))
print("Total de registros duplicados:", df.duplicated().sum())

print("\nVerificação concluída!")

# ==========================================
# QUESTÃO 3 - MAPEAMENTO DE ATIVOS
# ==========================================

print("\n===== MAPEAMENTO DE ATIVOS =====")

# 1. Separando somente os registros de moedas
dados_moedas = df[df["moeda"].notna()].copy()

# 2. Identificando as moedas e contando seus registros
quantidade_moedas = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda"])
    .size()
    .reset_index(name="quantidade_registros")
)

# 3. Organizando do maior para o menor volume de registros
quantidade_moedas = quantidade_moedas.sort_values(
    by="quantidade_registros",
    ascending=False
)

# 4. Exibindo a relação de moedas
print("\nMoedas identificadas e quantidade de registros:")
print(quantidade_moedas.to_string(index=False))

# 5. Exibindo a quantidade total de moedas
print("\nTotal de moedas estrangeiras identificadas:")
print(dados_moedas["codigo_moeda"].nunique())

# 6. Exibindo o total de registros analisados
print("\nTotal de registros de moedas:")
print(len(dados_moedas))

print("\nMapeamento de ativos concluído!")

# QUESTÃO 4 - COTAÇÃO MÉDIA POR MOEDA

# Filtrar somente os registros de moedas
dados_moedas = df[df["moeda"].notna()].copy()

# Calcular a cotação média de cada moeda
media_por_moeda = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda"])["cotacao_media"]
    .mean()
    .reset_index(name="cotacao_media_geral")
)

# Organizar da maior para a menor cotação média
media_por_moeda = media_por_moeda.sort_values(
    by="cotacao_media_geral",
    ascending=False
)

# Exibir os resultados
print("\nCotação média geral por moeda:")
print(media_por_moeda.to_string(index=False))

# QUESTÃO 5 - EXTREMOS HISTÓRICOS

# Selecionar somente Dólar Americano e Euro
moedas_selecionadas = df[
    df["codigo_moeda"].isin(["USD", "EUR"])
].copy()

# Identificar os extremos de cada moeda
for codigo in ["USD", "EUR"]:
    dados = moedas_selecionadas[
        moedas_selecionadas["codigo_moeda"] == codigo
    ]

    # Encontrar os índices das cotações máxima e mínima
    indice_maximo = dados["cotacao_media"].idxmax()
    indice_minimo = dados["cotacao_media"].idxmin()

    # Recuperar os registros correspondentes
    registro_maximo = dados.loc[indice_maximo]
    registro_minimo = dados.loc[indice_minimo]

    print(f"\n===== {registro_maximo['moeda']} ({codigo}) =====")

    print("\nMaior cotação:")
    print("Data:", registro_maximo["data_referencia"].strftime("%d/%m/%Y"))
    print("Valor:", registro_maximo["cotacao_media"])

    print("\nMenor cotação:")
    print("Data:", registro_minimo["data_referencia"].strftime("%d/%m/%Y"))
    print("Valor:", registro_minimo["cotacao_media"])

# QUESTÃO 6 - VARIAÇÃO PERCENTUAL ACUMULADA

# Selecionar somente os registros de moedas
dados_moedas = df[df["moeda"].notna()].copy()

# Ordenar os registros pela data
dados_moedas = dados_moedas.sort_values("data_referencia")

# Criar uma lista para armazenar os resultados
resultados_variacao = []

# Analisar cada moeda
for (codigo, nome), grupo in dados_moedas.groupby(
    ["codigo_moeda", "moeda"]
):
    # Organizar os registros da moeda por data
    grupo = grupo.sort_values("data_referencia")

    # Obter o primeiro e o último registro
    registro_inicial = grupo.iloc[0]
    registro_final = grupo.iloc[-1]

    # Obter as cotações inicial e final
    cotacao_inicial = registro_inicial["cotacao_media"]
    cotacao_final = registro_final["cotacao_media"]

    # Calcular a variação percentual acumulada
    variacao = (
        (cotacao_final / cotacao_inicial) - 1
    ) * 100

    # Guardar os resultados
    resultados_variacao.append({
        "codigo_moeda": codigo,
        "moeda": nome,
        "data_inicial": registro_inicial["data_referencia"],
        "cotacao_inicial": cotacao_inicial,
        "data_final": registro_final["data_referencia"],
        "cotacao_final": cotacao_final,
        "variacao_percentual_acumulada": variacao
    })

# Transformar os resultados em uma tabela
tabela_variacao = pd.DataFrame(resultados_variacao)

# Ordenar da maior valorização para a menor
tabela_variacao = tabela_variacao.sort_values(
    by="variacao_percentual_acumulada",
    ascending=False
)

# Exibir os resultados
print("\n===== VARIAÇÃO PERCENTUAL ACUMULADA =====")
print(tabela_variacao.to_string(index=False))

# Identificar a moeda que mais se valorizou
moeda_mais_valorizada = tabela_variacao.iloc[0]

print("\n===== MOEDA QUE MAIS SE VALORIZOU FRENTE AO REAL =====")
print("Moeda:", moeda_mais_valorizada["moeda"])
print("Código:", moeda_mais_valorizada["codigo_moeda"])
print(
    "Variação acumulada:",
    round(moeda_mais_valorizada["variacao_percentual_acumulada"], 2),
    "%"
)

# QUESTÃO 7 - COMPARATIVO BRL

import matplotlib.pyplot as plt

# Selecionar Dólar, Euro e Libra Esterlina
moedas_comparacao = df[
    df["codigo_moeda"].isin(["USD", "EUR", "GBP"])
].copy()

# Organizar os registros por data
moedas_comparacao = moedas_comparacao.sort_values(
    by="data_referencia"
)

# Criar o gráfico
plt.figure(figsize=(14, 7))

# Nomes das moedas
nomes_moedas = {
    "USD": "Dólar Americano (USD)",
    "EUR": "Euro (EUR)",
    "GBP": "Libra Esterlina (GBP)"
}

# Desenhar uma linha para cada moeda
for codigo, nome in nomes_moedas.items():

    dados = moedas_comparacao[
        moedas_comparacao["codigo_moeda"] == codigo
    ]

    plt.plot(
        dados["data_referencia"],
        dados["cotacao_media"],
        label=nome
    )

# Configurações do gráfico
plt.title("Comparativo Histórico de Moedas em Relação ao Real")
plt.xlabel("Data")
plt.ylabel("Cotação Média em Reais (R$)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Exibir resumo comparativo
print("\n===== COMPARATIVO HISTÓRICO BRL =====")

for codigo, nome in nomes_moedas.items():

    dados = moedas_comparacao[
        moedas_comparacao["codigo_moeda"] == codigo
    ].sort_values("data_referencia")

    cotacao_inicial = dados.iloc[0]["cotacao_media"]
    cotacao_final = dados.iloc[-1]["cotacao_media"]

    variacao = (
        (cotacao_final / cotacao_inicial) - 1
    ) * 100

    print(f"\n{nome}")
    print("Cotação inicial:", cotacao_inicial)
    print("Cotação final:", cotacao_final)
    print("Variação acumulada:", round(variacao, 2), "%")

# QUESTÃO 8 - ANÁLISE DE VOLATILIDADE

# Selecionar somente os registros de moedas
dados_moedas = df[df["moeda"].notna()].copy()

# ==========================================
# 1. MEDIDAS DE DISPERSÃO DE CADA MOEDA
# ==========================================

estatisticas_volatilidade = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda"])["cotacao_media"]
    .agg(["mean", "std", "var"])
    .reset_index()
)

# Renomear as colunas
estatisticas_volatilidade = estatisticas_volatilidade.rename(
    columns={
        "mean": "cotacao_media_geral",
        "std": "desvio_padrao",
        "var": "variancia"
    }
)

# Organizar da maior para a menor dispersão
estatisticas_volatilidade = estatisticas_volatilidade.sort_values(
    by="desvio_padrao",
    ascending=False
)

print("\n===== VOLATILIDADE GERAL POR MOEDA =====")
print(estatisticas_volatilidade.to_string(index=False))

# ==========================================
# 2. VOLATILIDADE MENSAL
# ==========================================

# Criar uma coluna com o ano e o mês
dados_moedas["ano_mes"] = (
    dados_moedas["data_referencia"].dt.to_period("M")
)

# Calcular o desvio padrão mensal de cada moeda
volatilidade_mensal = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda", "ano_mes"])["cotacao_media"]
    .std()
    .reset_index(name="desvio_padrao_mensal")
)

# Identificar o mês de maior volatilidade de cada moeda
indices_maior_volatilidade = (
    volatilidade_mensal
    .groupby("codigo_moeda")["desvio_padrao_mensal"]
    .idxmax()
)

maiores_volatilidades = volatilidade_mensal.loc[
    indices_maior_volatilidade
].sort_values(
    by="desvio_padrao_mensal",
    ascending=False
)

print("\n===== MESES DE MAIOR VOLATILIDADE POR MOEDA =====")
print(maiores_volatilidades.to_string(index=False))

# ==========================================
# 3. MAIOR OSCILAÇÃO ENTRE TODAS AS MOEDAS
# ==========================================

maior_mes = maiores_volatilidades.iloc[0]

print("\n===== MAIOR VOLATILIDADE IDENTIFICADA =====")
print("Moeda:", maior_mes["moeda"])
print("Código:", maior_mes["codigo_moeda"])
print("Mês:", maior_mes["ano_mes"])
print(
    "Desvio padrão mensal:",
    round(maior_mes["desvio_padrao_mensal"], 6)
)

# QUESTÃO 8 - ANÁLISE DE VOLATILIDADE

# Selecionar somente os registros de moedas
dados_moedas = df[df["moeda"].notna()].copy()

# ==========================================
# 1. MEDIDAS DE DISPERSÃO DE CADA MOEDA
# ==========================================

estatisticas_volatilidade = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda"])["cotacao_media"]
    .agg(["mean", "std", "var"])
    .reset_index()
)

# Renomear as colunas
estatisticas_volatilidade = estatisticas_volatilidade.rename(
    columns={
        "mean": "cotacao_media_geral",
        "std": "desvio_padrao",
        "var": "variancia"
    }
)

# Organizar da maior para a menor dispersão
estatisticas_volatilidade = estatisticas_volatilidade.sort_values(
    by="desvio_padrao",
    ascending=False
)

print("\n===== VOLATILIDADE GERAL POR MOEDA =====")
print(estatisticas_volatilidade.to_string(index=False))

# ==========================================
# 2. VOLATILIDADE MENSAL
# ==========================================

# Criar uma coluna com o ano e o mês
dados_moedas["ano_mes"] = (
    dados_moedas["data_referencia"].dt.to_period("M")
)

# Calcular o desvio padrão mensal de cada moeda
volatilidade_mensal = (
    dados_moedas
    .groupby(["codigo_moeda", "moeda", "ano_mes"])["cotacao_media"]
    .std()
    .reset_index(name="desvio_padrao_mensal")
)

# Identificar o mês de maior volatilidade de cada moeda
indices_maior_volatilidade = (
    volatilidade_mensal
    .groupby("codigo_moeda")["desvio_padrao_mensal"]
    .idxmax()
)

maiores_volatilidades = volatilidade_mensal.loc[
    indices_maior_volatilidade
].sort_values(
    by="desvio_padrao_mensal",
    ascending=False
)

print("\n===== MESES DE MAIOR VOLATILIDADE POR MOEDA =====")
print(maiores_volatilidades.to_string(index=False))

# ==========================================
# 3. MAIOR OSCILAÇÃO ENTRE TODAS AS MOEDAS
# ==========================================

maior_mes = maiores_volatilidades.iloc[0]

print("\n===== MAIOR VOLATILIDADE IDENTIFICADA =====")
print("Moeda:", maior_mes["moeda"])
print("Código:", maior_mes["codigo_moeda"])
print("Mês:", maior_mes["ano_mes"])
print(
    "Desvio padrão mensal:",
    round(maior_mes["desvio_padrao_mensal"], 6)
)

# QUESTÃO 9 - CONTEXTO MACROECONÔMICO

# Separar os registros de indicadores econômicos
dados_indicadores = df[
    df["indicador_economico"].notna()
].copy()

print("\n===== INDICADORES ECONÔMICOS IDENTIFICADOS =====")

# Quantidade de registros por indicador e periodicidade
resumo_indicadores = (
    dados_indicadores
    .groupby(["indicador_economico", "periodicidade"])
    .size()
    .reset_index(name="quantidade_registros")
)

print(resumo_indicadores.to_string(index=False))

# Verificar o período disponível para os indicadores
print("\nData inicial dos indicadores:")
print(dados_indicadores["data_referencia"].min())

print("\nData final dos indicadores:")
print(dados_indicadores["data_referencia"].max())

# Verificar a quantidade total de registros
print("\nTotal de registros de indicadores:")
print(len(dados_indicadores))

# Verificar a periodicidade das cotações do dólar
dados_dolar = df[
    df["codigo_moeda"] == "USD"
].copy()

print("\n===== INFORMAÇÕES DO DÓLAR =====")
print("Total de registros:", len(dados_dolar))
print(
    "Data inicial:",
    dados_dolar["data_referencia"].min()
)
print(
    "Data final:",
    dados_dolar["data_referencia"].max()
)

print("\nDiagnóstico dos indicadores concluído!")

# ==========================================
# 2. COMPARAÇÃO DOS INDICADORES COM O DÓLAR
# ==========================================

# Criar uma coluna que identifica o ano e o mês
dados_indicadores["ano_mes"] = (
    dados_indicadores["data_referencia"].dt.to_period("M")
)

# ------------------------------------------
# IPCA: organizar os valores mensais
# ------------------------------------------

dados_ipca = dados_indicadores[
    dados_indicadores["indicador_economico"] == "IPCA"
].copy()

ipca_mensal = (
    dados_ipca
    .groupby("ano_mes")["valor_indicador"]
    .mean()
)

# ------------------------------------------
# SELIC: organizar os registros por mês
# ------------------------------------------

dados_selic = dados_indicadores[
    dados_indicadores["indicador_economico"] == "Taxa Selic Meta"
].copy()

selic_mensal = (
    dados_selic
    .groupby("ano_mes")["valor_indicador"]
    .last()
)

# Criar uma sequência mensal completa
meses_completos = pd.period_range(
    start=selic_mensal.index.min(),
    end=selic_mensal.index.max(),
    freq="M"
)

# Preencher os meses sem reunião com o último valor disponível
selic_mensal = (
    selic_mensal
    .reindex(meses_completos)
    .ffill()
)

# ------------------------------------------
# DÓLAR: calcular a cotação média mensal
# ------------------------------------------

dados_dolar = df[
    df["codigo_moeda"] == "USD"
].copy()

dados_dolar["ano_mes"] = (
    dados_dolar["data_referencia"].dt.to_period("M")
)

dolar_mensal = (
    dados_dolar
    .groupby("ano_mes")["cotacao_media"]
    .mean()
)

# Calcular a variação percentual mensal do dólar
variacao_dolar = dolar_mensal.pct_change() * 100

# ------------------------------------------
# 3. JUNTAR AS TRÊS SÉRIES
# ------------------------------------------

comparativo = pd.DataFrame({
    "variacao_dolar": variacao_dolar,
    "ipca": ipca_mensal,
    "selic": selic_mensal
})

# Calcular a mudança mensal da Selic em pontos percentuais
comparativo["variacao_selic"] = comparativo["selic"].diff()

# Remover meses sem informações suficientes
comparativo = comparativo.dropna(
    subset=["variacao_dolar", "ipca", "variacao_selic"]
)

print("\n===== COMPARAÇÃO MENSAL DOS INDICADORES =====")
print(comparativo.head(10).to_string())

print("\nQuantidade de meses comparados:")
print(len(comparativo))

# ------------------------------------------
# 4. PADRONIZAR OS DADOS PARA O GRÁFICO
# ------------------------------------------

series_comparacao = comparativo[
    ["variacao_dolar", "ipca", "variacao_selic"]
]

dados_padronizados = (
    series_comparacao - series_comparacao.mean()
) / series_comparacao.std()

# ------------------------------------------
# 5. CALCULAR AS CORRELAÇÕES
# ------------------------------------------

correlacoes = comparativo[
    ["variacao_dolar", "ipca", "variacao_selic"]
].corr()

print("\n===== CORRELAÇÃO COM A VARIAÇÃO DO DÓLAR =====")
print(correlacoes["variacao_dolar"].to_string())

# ------------------------------------------
# 6. GERAR GRÁFICO COMPARATIVO
# ------------------------------------------

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))

plt.plot(
    dados_padronizados.index.to_timestamp(),
    dados_padronizados["variacao_dolar"],
    label="Variação mensal do Dólar",
    color="blue"
)

plt.plot(
    dados_padronizados.index.to_timestamp(),
    dados_padronizados["ipca"],
    label="IPCA mensal",
    color="orange"
)

plt.plot(
    dados_padronizados.index.to_timestamp(),
    dados_padronizados["variacao_selic"],
    label="Variação mensal da Selic",
    color="green"
)

plt.title("Indicadores Macroeconômicos e Variação do Dólar")
plt.xlabel("Data")
plt.ylabel("Valores padronizados (desvios padrão)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nAnálise macroeconômica concluída!")
# ==========================================
# QUESTÃO 10 - REPRESENTAÇÃO GRÁFICA
# ==========================================

import matplotlib.pyplot as plt

# Separando os registros de moedas
q10_moedas = df[df["moeda"].notna()].copy()

# Ordenando os dados pelas datas
q10_moedas = q10_moedas.sort_values("data_referencia")


# ==========================================
# GRÁFICO 1 - EVOLUÇÃO HISTÓRICA DAS MOEDAS
# ==========================================

q10_principais = q10_moedas[
    q10_moedas["codigo_moeda"].isin(["USD", "EUR", "GBP"])
]

plt.figure(figsize=(14, 6))

for codigo in ["USD", "EUR", "GBP"]:
    dados = q10_principais[
        q10_principais["codigo_moeda"] == codigo
    ]

    nome = dados["moeda"].iloc[0]

    plt.plot(
        dados["data_referencia"],
        dados["cotacao_media"],
        label=f"{nome} ({codigo})"
    )

plt.title("Evolução Histórica das Principais Moedas")
plt.xlabel("Data")
plt.ylabel("Cotação Média em Reais (R$)")
plt.legend(title="Moedas")
plt.grid(True)
plt.tight_layout()
plt.show()


# ==========================================
# GRÁFICO 2 - COTAÇÃO MÉDIA POR MOEDA
# ==========================================

q10_media = (
    q10_moedas
    .groupby(["codigo_moeda", "moeda"])["cotacao_media"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))

q10_media.plot(
    kind="bar",
    label="Cotação média"
)

plt.title("Cotação Média Geral por Moeda")
plt.xlabel("Moeda")
plt.ylabel("Cotação Média em Reais (R$)")
plt.legend()
plt.grid(axis="y")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==========================================
# GRÁFICO 3 - VARIAÇÃO PERCENTUAL ACUMULADA
# ==========================================

q10_resultados = []

for codigo, grupo in q10_moedas.groupby("codigo_moeda"):

    grupo = grupo.sort_values("data_referencia")

    cotacao_inicial = grupo["cotacao_media"].iloc[0]
    cotacao_final = grupo["cotacao_media"].iloc[-1]

    variacao = (
        (cotacao_final - cotacao_inicial)
        / cotacao_inicial
    ) * 100

    q10_resultados.append({
        "codigo_moeda": codigo,
        "variacao_acumulada": variacao
    })

q10_variacao = pd.DataFrame(q10_resultados)

q10_variacao = q10_variacao.sort_values(
    "variacao_acumulada",
    ascending=False
)

plt.figure(figsize=(12, 6))

plt.bar(
    q10_variacao["codigo_moeda"],
    q10_variacao["variacao_acumulada"],
    label="Variação acumulada (%)"
)

plt.axhline(y=0, color="black", linewidth=0.8)

plt.title("Valorização e Desvalorização das Moedas")
plt.xlabel("Código da Moeda")
plt.ylabel("Variação Acumulada (%)")
plt.legend()
plt.grid(axis="y")
plt.tight_layout()
plt.show()


# ==========================================
# GRÁFICO 4 - VOLATILIDADE POR MOEDA
# ==========================================

q10_volatilidade = (
    q10_moedas
    .groupby(["codigo_moeda", "moeda"])["cotacao_media"]
    .std()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))

q10_volatilidade.plot(
    kind="bar",
    label="Desvio padrão"
)

plt.title("Volatilidade das Cotações Médias por Moeda")
plt.xlabel("Moeda")
plt.ylabel("Desvio Padrão")
plt.legend()
plt.grid(axis="y")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


print("\n===== QUESTÃO 10 CONCLUÍDA =====")
print("Os quatro gráficos foram gerados com sucesso!")

# ==========================================
# QUESTÃO 11 - ESTUDO APLICADO
# ==========================================

import matplotlib.pyplot as plt

# 1. Selecionar somente os registros de moedas
q11_dados = df[df["moeda"].notna()].copy()

# 2. Definir o período de análise
# Incluímos dezembro de 2016 como referência
# para calcular a variação de janeiro de 2017.

q11_dados = q11_dados[
    (q11_dados["data_referencia"] >= "2016-12-01") &
    (q11_dados["data_referencia"] < "2022-01-01")
].copy()

# 3. Criar uma coluna com o mês de cada registro
q11_dados["mes"] = (
    q11_dados["data_referencia"].dt.to_period("M")
)

# 4. Calcular a cotação média mensal de cada moeda
q11_mensal = (
    q11_dados
    .groupby(["codigo_moeda", "moeda", "mes"])["cotacao_media"]
    .mean()
    .reset_index(name="cotacao_media_mensal")
)

# 5. Ordenar os dados cronologicamente
q11_mensal = q11_mensal.sort_values(
    ["codigo_moeda", "mes"]
)

# 6. Calcular a variação percentual mensal
q11_mensal["variacao_mensal"] = (
    q11_mensal
    .groupby("codigo_moeda")["cotacao_media_mensal"]
    .pct_change() * 100
)

# 7. Manter somente os cinco anos escolhidos
q11_mensal = q11_mensal[
    (q11_mensal["mes"] >= "2017-01") &
    (q11_mensal["mes"] <= "2021-12")
].copy()

# 8. Calcular as métricas estatísticas de cada moeda
q11_resultados = (
    q11_mensal
    .groupby(["codigo_moeda", "moeda"])
    .agg(
        desvio_padrao=("variacao_mensal", "std"),
        variancia=("variacao_mensal", "var"),
        variacao_media_mensal=("variacao_mensal", "mean"),
        cotacao_inicial=("cotacao_media_mensal", "first"),
        cotacao_final=("cotacao_media_mensal", "last")
    )
    .reset_index()
)

# 9. Calcular a variação percentual acumulada
q11_resultados["variacao_acumulada"] = (
    (
        q11_resultados["cotacao_final"]
        - q11_resultados["cotacao_inicial"]
    )
    / q11_resultados["cotacao_inicial"]
) * 100

# 10. Ordenar da menor para a maior volatilidade
q11_resultados = q11_resultados.sort_values(
    "desvio_padrao"
)

print("\n===== ESTUDO APLICADO - PERÍODO 2017 A 2021 =====")
print("\nMétricas estatísticas por moeda:")
print(q11_resultados.to_string(index=False))

# 11. Identificar a moeda mais estável
moeda_segura = q11_resultados.iloc[0]

# 12. Identificar a moeda mais volátil
moeda_especulativa = q11_resultados.iloc[-1]

print("\n===== VEREDITO DA INVESTIGAÇÃO =====")

print("\nMOEDA MAIS ESTÁVEL (MENOR RISCO):")
print("Moeda:", moeda_segura["moeda"])
print("Código:", moeda_segura["codigo_moeda"])
print("Desvio padrão mensal:", round(
    moeda_segura["desvio_padrao"], 4
), "%")
print("Variação acumulada:", round(
    moeda_segura["variacao_acumulada"], 2
), "%")

print("\nMOEDA MAIS VOLÁTIL (MAIOR RISCO):")
print("Moeda:", moeda_especulativa["moeda"])
print("Código:", moeda_especulativa["codigo_moeda"])
print("Desvio padrão mensal:", round(
    moeda_especulativa["desvio_padrao"], 4
), "%")
print("Variação acumulada:", round(
    moeda_especulativa["variacao_acumulada"], 2
), "%")

# 13. Preparar os dados para o gráfico
q11_grafico = q11_mensal.pivot(
    index="mes",
    columns="codigo_moeda",
    values="variacao_mensal"
)

# Selecionar somente a moeda mais estável
# e a moeda mais volátil
codigos_selecionados = [
    moeda_segura["codigo_moeda"],
    moeda_especulativa["codigo_moeda"]
]

q11_grafico = q11_grafico[codigos_selecionados]

q11_grafico.index = q11_grafico.index.to_timestamp()

# 14. Construir o gráfico comparativo
plt.figure(figsize=(14, 6))

for codigo in codigos_selecionados:
    nome = q11_mensal[
        q11_mensal["codigo_moeda"] == codigo
    ]["moeda"].iloc[0]

    plt.plot(
        q11_grafico.index,
        q11_grafico[codigo],
        label=f"{nome} ({codigo})"
    )

plt.axhline(y=0, color="black", linewidth=0.8)

plt.title(
    "Comparação de Volatilidade Cambial - 2017 a 2021"
)
plt.xlabel("Data")
plt.ylabel("Variação Percentual Mensal (%)")
plt.legend(title="Moedas")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nEstudo aplicado concluído!")
# ===== GRÁFICO COMPARATIVO DO ESTUDO APLICADO =====

import matplotlib.pyplot as plt

# Dados estatísticos obtidos na análise de 2017 a 2021
grafico_estudo = pd.DataFrame({
    "codigo_moeda": [
        "ARS", "CHF", "USD", "EUR", "CAD",
        "JPY", "AUD", "MXN", "CNY", "GBP"
    ],
    "desvio_padrao": [
        3.969274, 4.113483, 4.179181, 4.264060, 4.374742,
        4.480761, 4.480840, 4.544344, 4.847317, 5.015133
    ]
})

grafico_estudo = grafico_estudo.sort_values(
    by="desvio_padrao"
)

plt.figure(figsize=(11, 6))

plt.bar(
    grafico_estudo["codigo_moeda"],
    grafico_estudo["desvio_padrao"],
    label="Desvio padrão mensal (%)"
)

plt.title("Comparação de Volatilidade das Moedas (2017–2021)")
plt.xlabel("Código da moeda")
plt.ylabel("Desvio padrão mensal (%)")
plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()