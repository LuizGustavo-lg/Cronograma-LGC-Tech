import pandas as pd
import plotly.express as px
import plotly.offline as pyo
from dias import obter_dias_semana


df = pd.read_excel('Cronograma.xlsx')

df_gantt = df[['Tarefa', 'Data de início', 'Data de término', 'Proprietário', 'Observações', 'Equipe', 'Tipo', 'Data de repetição']].copy()

df_gantt['Data de início'] = pd.to_datetime(df_gantt['Data de início'])
df_gantt['Data de término'] = pd.to_datetime(df_gantt["Data de término"])


df_gantt['Data de término'] = df_gantt['Data de término'].apply(lambda x: x.replace(hour=23, minute=59))


def add_new(x):
    global df_gantt

    for d_semana in x['Data de repetição'].split(', '):
        dias_list = obter_dias_semana(x['Data de início'], x['Data de término'], d_semana)
        
        for d in dias_list:
            t = pd.DataFrame({'Tarefa': x['Tarefa'],
                    'Data de início': d,
                    'Data de término': d.replace(hour=23, minute=59),
                    'Proprietário': x['Proprietário'], 
                    'Observações': x['Observações'],
                    'Equipe': x['Equipe'], 
                    'Tipo': x['Tipo'], 
                    'Data de repetição': x['Data de repetição']}, index=[0])

            df_gantt = pd.concat([df_gantt, t])
    return x


id_exclusion = df_gantt[df_gantt['Data de repetição'].isnull().__invert__()].apply(add_new, axis=1).index

df_gantt.drop(id_exclusion, inplace=True)
df_gantt.dropna(subset=['Data de início', 'Data de término'], inplace=True)

df_gantt['Equipe Responsavel'] = df_gantt['Equipe'].apply(lambda x: x.split(', ')[0])

fig = px.timeline(
    df_gantt,
    x_start='Data de início',
    x_end='Data de término',
    y='Tarefa',
    color='Equipe Responsavel',
    hover_name='Observações',
    title='Cronograma LGC-TECH',
    text='Proprietário',
    hover_data=['Equipe', 'Tipo']
)


fig.update_yaxes(categoryorder='total ascending')  # Ordenar as tarefas
fig.update_layout(xaxis_title='Data', yaxis_title='Tarefa')


# fig.show()
pyo.plot(fig, filename='cronograma.html')
