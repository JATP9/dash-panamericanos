import dash
from dash import html, dcc
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import os

# Conexión a MongoDB Atlas
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["Panamericanos"]
collection = db["Medallistas"]

# Leer datos desde MongoDB y convertirlos en DataFrame
data = list(collection.find({}, {"_id": 0}))  # excluye _id
df = pd.DataFrame(data)

# Cierre de conexión
client.close()

# Inicializar la app de Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Medallistas Panamericanos"

# Layout del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Medallistas Panamericanos", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(
            id="dropdown-pais",
            options=[{"label": pais, "value": pais} for pais in df["País"].unique()],
            value=df["País"].unique()[0],
            placeholder="Selecciona un país"
        ),
    ], style={"width": "50%", "margin": "auto"}),

    dcc.Graph(id="grafico-medallas")
])

# Callback para actualizar el gráfico según el país
@app.callback(
    dash.dependencies.Output("grafico-medallas", "figure"),
    [dash.dependencies.Input("dropdown-pais", "value")]
)
def actualizar_grafico(pais):
    df_filtrado = df[df["País"] == pais]
    fig = px.histogram(df_filtrado, x="Medalla", color="Medalla",
                       title=f"Medallas de {pais}", barmode="group")
    return fig

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

