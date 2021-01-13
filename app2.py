import geopandas
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

#world = geopandas.read_file('Data/OrigOoklaData/gps_mobile_tiles.shp')

#print(world.head())
#print(world.columns)

#finland = world[world['quadkey'].str.startswith('120120033')]

#print(finland)
#print(finland.columns)
#finland.to_file("finland.shp")

finland = geopandas.read_file('Data/FinlandData/finland.shp')
finland['avg_d_mbps'] = finland['avg_d_kbps']/1000
#print(finland.head())
#print(finland.columns)


#Quantiles for finland['avg_d_mbps'] in order to plot 'avg_d_mbps' in ranges
bins = []
for i in range(1,10,1):
    bins.append(round(finland['avg_d_mbps'].quantile(i/10),1))

bins.insert(0, 0)
bins.append(finland['avg_d_mbps'].max())
labels = ['<{}'.format(bins[1]),
        '>={} & <{}'.format(bins[1],bins[2]),
        '>={} & <{}'.format(bins[2],bins[3]),
        '>={} & <{}'.format(bins[3],bins[4]),
        '>={} & <{}'.format(bins[4],bins[5]),
        '>={} & <{}'.format(bins[5],bins[6]),
        '>={} & <{}'.format(bins[6],bins[7]),
        '>={} & <{}'.format(bins[7],bins[8]),
        '>={} & <{}'.format(bins[8],bins[9]),
        '>={}'.format(bins[9])]

finland['avg_d_mbps_ranges'] = pd.cut(finland['avg_d_mbps'], bins=bins, labels=labels)
finland = finland.sort_values(by=['avg_d_mbps'])
finland =finland.reset_index()
#print(finland['avg_d_mbps_ranges'].unique())

#finland = finland.head(1000) # to limit amount of data plotted

fig = px.choropleth_mapbox(finland,
                geojson=finland.geometry,
                locations=finland.index,
                color="avg_d_mbps_ranges",
                color_discrete_sequence= px.colors.sequential.Turbo_r,
                opacity=0.5,
                hover_data = ['avg_d_mbps_ranges','avg_d_mbps','avg_u_kbps','tests','devices'],
                custom_data = ['avg_d_mbps','quadkey'],
                center = {'lat':60.2932,'lon':25.0377},
                zoom = 12,
                mapbox_style="open-street-map")
#fig.update_geos(fitbounds="locations", visible=False)
#fig.show()
#fig.update_geos(fitbounds="locations", visible=False)
#fig.show()

colors = ['rgb(84,160,143)',] * finland.shape[0]
bar_chart = go.Figure(data=[go.Bar(x=finland['quadkey'], y=finland['avg_d_mbps'],marker_color=colors)])

bar_chart.update_layout(yaxis={'title':'avg_d_mbps','range':[0,finland['avg_d_mbps'].max()],'showgrid':True,'gridcolor':'rgb(216,216,220)'},
                        xaxis={'categoryorder':'total descending','showgrid':True,'visible':False},
                        plot_bgcolor='rgba(0,0,0,0)',
                        title={'text':'<b>avg_d_mpbs per tile<b>','font':{'size':18.72}})



app = dash.Dash()
#USERNAME_PASSWORD_PAIRS = [['XXXX', 'XXXX']]
#auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
#server = app.server

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/omnitele-favicon-posi.svg", height="20px",style={'margin-left':10}),
        html.A('Speedtest by Ookla Mobile Network',className="header"),
    ]),

    html.Div([

        html.Div([
            html.A('Filters:',style={'margin-top':'10px'}),

            dcc.Dropdown(options=[
                    {'label': '2021', 'value': '21'},
                    {'label': '2022', 'value': '22'},
                    {'label': '2023', 'value': '23'}
                ],placeholder="Target year",className="filters"
            ),

            dcc.Dropdown(options=[
                    {'label': 'Option1', 'value': 'a'},
                    {'label': 'Option2', 'value': 'b'},
                    {'label': 'Option3', 'value': 'c: '}
                ],placeholder="Filter2",className="filters"
            ),

            dcc.Dropdown(options=[
                    {'label': 'Option1', 'value': 'd'},
                    {'label': 'Option2', 'value': 'e'},
                    {'label': 'Option3', 'value': 'f'}
                ],placeholder="Filter3",className="filters"
            ),

            html.Div([html.Button("", id="btn",className="download"), Download(id="download")],className="filters")

        ],className="main-filters_row"),

 ],className="filters_row"),
        html.Div([
            dcc.Markdown('''
                    ### This dashbord was built using [Ookla Open Dataset](https://registry.opendata.aws/speedtest-global-performance/).
                    #### Used data shows mobile (cellular) network performance metrics in zoom level 16 web mercator tiles (approximately 610.8 meters by 610.8 meters at the equator).
                ''')],style={'margin-left':'10px'},
            ),

        html.Div([
            html.Img(src="/assets/indicator.png",className="overviewcard"),
            html.Img(src="/assets/indicator.png",className="overviewcard"),
            html.Img(src="/assets/indicator.png",className="overviewcard"),
            html.Img(src="/assets/indicator.png",className="overviewcard"),
        ],className="main-overview"),

        html.Div([
            dcc.Graph(id='map',figure=fig,className="card"),
            html.A(id='counter',children='Avg_d_mbps in the tile you hover over is X Mpbs.',className="card"),
            dcc.Graph(id='bar_chart',figure=bar_chart,className="card"),
        ],className="main-cards"),

])



@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def generate_csv(n_nlicks):
    if n_nlicks>=1:
        return send_data_frame(finland.to_csv, filename="some_name.csv")


@app.callback(Output('counter', 'children'),
              [Input('map', 'hoverData')])
def find_counter(hoverData):
    mean = hoverData['points'][0]['customdata'][0]
    return 'Avg_d_mbps in the tile you hover over is {} Mpbs.'.format(mean)


@app.callback(Output('bar_chart', 'figure'),
              [Input('map', 'hoverData')])
def callback_graph(hoverData):
    v_index = hoverData['points'][0]['location']
    colors = ['rgb(84,160,143)',] * finland.shape[0]
    colors[v_index] = 'rgb(249,158,58)'
    bar_chart = go.Figure(data=[go.Bar(x=finland['quadkey'], y=finland['avg_d_mbps'],marker_color=colors)])
    bar_chart.update_layout(yaxis={'title':'avg_d_mbps','range':[0,finland['avg_d_mbps'].max()],'showgrid':True,'gridcolor':'rgb(216,216,220)'},
                        xaxis={'categoryorder':'total descending','showgrid':True,'visible':False},
                        plot_bgcolor='rgba(0,0,0,0)',
                        title={'text':'<b>avg_d_mpbs per tile<b>','font':{'size':18.72}})

    return bar_chart




if __name__ == '__main__':
    app.run_server()  # Turn off reloader if inside Jupyter
