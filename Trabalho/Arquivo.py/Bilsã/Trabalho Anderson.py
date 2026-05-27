import psycopg2
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# CONEXÃO 


conexao = psycopg2.connect(
    host="localhost",
    database="BilzarPub",
    user="postgres",
    password="Maniko12!",
    port="5432"
)

# ==========================
# FATURAMENTO POR MÊS
# ==========================

sql_faturamento = """
SELECT
    EXTRACT(MONTH FROM data_festa) AS mes,
    SUM(valor_total) AS faturamento
FROM festas
GROUP BY mes
ORDER BY mes;
"""

df_faturamento = pd.read_sql(sql_faturamento, conexao)

meses = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez"
}

df_faturamento["mes"] = (
    df_faturamento["mes"]
    .astype(int)
    .map(meses)
)

# ==========================
# USO DOS SALÕES
# ==========================

sql_saloes = """
SELECT
    s.nome_salao,
    COUNT(*) AS total_festas
FROM festas f
JOIN saloes s ON f.id_salao = s.id_salao
GROUP BY s.nome_salao
ORDER BY total_festas DESC;
"""

df_saloes = pd.read_sql(sql_saloes, conexao)

# ==========================
# QUANTIDADE DE FESTAS POR MÊS
# ==========================

sql_festas_mes = """
SELECT
    EXTRACT(MONTH FROM data_festa) AS mes,
    COUNT(*) AS total_festas
FROM festas
GROUP BY mes
ORDER BY mes;
"""

df_festas_mes = pd.read_sql(sql_festas_mes, conexao)

df_festas_mes["mes"] = (
    df_festas_mes["mes"]
    .astype(int)
    .map(meses)
)

# ==========================
# TEMAS MAIS POPULARES
# ==========================

sql_temas = """
SELECT
    tema,
    COUNT(*) AS quantidade
FROM festas
GROUP BY tema
ORDER BY quantidade DESC;
"""

df_temas = pd.read_sql(sql_temas, conexao)



dashboard = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "bar"}, {"type": "pie"}],
        [{"type": "scatter"}, {"type": "bar"}]
    ],
    subplot_titles=(
        "Faturamento por Mês",
        "Uso dos Salões",
        "Quantidade de Festas por Mês",
        "Temas Mais Populares"
    )
)


dashboard.add_trace(
    go.Bar(
        x=df_faturamento["mes"],
        y=df_faturamento["faturamento"],
        name="Faturamento"
    ),
    row=1,
    col=1
)


dashboard.add_trace(
    go.Pie(
        labels=df_saloes["nome_salao"],
        values=df_saloes["total_festas"],
        textinfo="label+percent"
    ),
    row=1,
    col=2
)


dashboard.add_trace(
    go.Scatter(
        x=df_festas_mes["mes"],
        y=df_festas_mes["total_festas"],
        mode="lines+markers",
        name="Festas"
    ),
    row=2,
    col=1
)


dashboard.add_trace(
    go.Bar(
        x=df_temas["tema"],
        y=df_temas["quantidade"],
        name="Temas"
    ),
    row=2,
    col=2
)


dashboard.update_layout(
    title="Dashboard BilzarBar",
    height=900,
    width=1400,
    showlegend=False
)


dashboard.show()

conexao.close()
