import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
file = 'data/XGBoost/15-24_df_for_pred.tsv'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# data frame 是长数据格式
# df = pd.DataFrame({
#     "姓名": ["LeBron", "Steph", "Harden", "姚明", "易建联", "王治郅"],
#     "身高": [206, 192, 196, 226, 213, 214],
#     "位置": ["SF", "PG", "PG", "C", "PF", "C"]
# })
df = pd.read_csv(file,sep='\t')

# fig = px.bar(df, x="姓名", y="身高", color="位置", barmode="group")
fig = px.scatter(df, x="Box office max", y="Budget max")
fig.update_layout(
    xaxis_type='log',
    yaxis_type='log',
    xaxis_title="Box office max (Log Scale)",
    yaxis_title="Budget max (Log Scale)"
)

fig_1 = px.histogram(df,x="Box office max",nbins=200)
fig_1.update_layout(
    # xaxis_type='log',
    yaxis_type='log',
    xaxis_title="Box office max"
)

file1 = 'data/PCA/15-24_df_genres_cutWord_multi_lines.tsv'
df1 = pd.read_csv(file1,sep='\t')
fig_2 = px.bar(df1, y="Box office max", x="genres")#, color='genres')
fig_2.update_layout(
    # xaxis_type='log',
    yaxis_type='log',
    yaxis_title="Box office (Log Scale)",
    xaxis_title="Genres"
)


app.layout = html.Div(children=[
    html.H1(children='Boxoffice-Budget'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='boxoffice-budget',
        figure=fig
    ),
    dcc.Graph(
        id='boxoffice',
        figure=fig_1
    ),
    dcc.Graph(
        id='boxoffice-budget-genres',
        figure=fig_2
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)