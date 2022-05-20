from dash import Dash, dcc ,Output ,Input
import dash_bootstrap_components as dbc
from numpy import NaN
import plotly.express as px
import pandas as pd
from datetime import datetime


excel_file = 'src/tests.xlsx'
df = pd.read_excel(excel_file)

for i in range(len(df['Date Application Submitted'])):
    if df['Date Application Submitted'][i] is not NaN:        
        df['Date Application Submitted'][i]=datetime.strptime(df['Date Application Submitted'][i], '%m %d %Y').strftime('%Y-%m-%d')   
         
    if df['Date Closed'][i] is not NaN:        
        df['Date Closed'][i]=datetime.strptime(df['Date Closed'][i], '%m %d %Y').strftime('%Y-%m-%d')  
    
    if df['Date Application Submitted'][i] is not NaN and df['Date Closed'][i] is NaN: 
        df['Date Closed'][i] = datetime.today().strftime('%Y-%m-%d')

# colors = {'TD': (0,128,0),
#           'AMEX': (1, 0.9, 0.16),
#           'MBNA':  	(0,255,255),
#           'CIBC': (128,0,0),
#           'RBC':  (0,0,255),
#           'SCOTIA' :(0,255,0),
#           'AMEX(usa)': (128,0,128)}

#plotly.offline.plot(fig, filename="testing.html")

#build components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

mytitle=dcc.Markdown(children='Credit card tracker')
mygraph = dcc.Graph(id='my-graph',style={'width': '100vh', 'height': '100vh'}, figure={})
dropdown = dcc.Dropdown(options=['Bankname','Person'],value='Person',clearable=False)


# #Customize layout
app.layout =dbc.Container([mytitle,mygraph,dropdown])

@app.callback(
    Output(mygraph ,component_property='figure'),
    Input(dropdown, component_property='value')
)

def update_title(user_input):
    if user_input == 'Person':
        fig = px.timeline(df, x_start = df['Date Application Submitted'] ,
                        x_end = df['Date Closed'],
                        y = df['Card Name'],
                        color=df['Card Personal']) 
        fig.update_yaxes(autorange="reversed")
        
    if user_input == 'Bankname':
        fig = px.timeline(df, x_start = df['Date Application Submitted'] ,
                        x_end = df['Date Closed'],
                        y = df['Card Name'],
                        color=df['Bank Name']) 
        fig.update_yaxes(autorange="reversed") 
        
    return fig
    

if __name__ == '__main__':
    app.run_server(port=8051,debug=True, use_reloader=True)