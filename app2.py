import geopandas
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import Input, Output

USERNAME_PASSWORD_PAIRS = [
    ['Voropaeva', 'AGF8453m27!']
]


#orld = geopandas.read_file('gps_mobile_tiles.shx')

#print(world.head())
#print(world.columns)

#finland = world[world['quadkey'].str.startswith('120120033')]

#print(finland)
#print(finland.columns)
#finland.to_file("finland.shp")

finland = geopandas.read_file('finland.shx')

#print(finland.head())
#print(finland.columns)


finland['avg_d_mbps'] = finland['avg_d_kbps']/1000

#Quantiles for finland['avg_d_mbps'] in order to plot 'avg_d_mbps' in ranges
avg_d_q1 = round(finland['avg_d_mbps'].quantile(.1),1)
avg_d_q2 = round(finland['avg_d_mbps'].quantile(.2),1)
avg_d_q3 = round(finland['avg_d_mbps'].quantile(.3),1)
avg_d_q4 = round(finland['avg_d_mbps'].quantile(.4),1)
avg_d_q5 = round(finland['avg_d_mbps'].quantile(.5),1)
avg_d_q6 = round(finland['avg_d_mbps'].quantile(.6),1)
avg_d_q7 = round(finland['avg_d_mbps'].quantile(.7),1)
avg_d_q8 = round(finland['avg_d_mbps'].quantile(.8),1)
avg_d_q9 = round(finland['avg_d_mbps'].quantile(.9),1)

bins = [0, avg_d_q1, avg_d_q2, avg_d_q3, avg_d_q4, avg_d_q5, avg_d_q6, avg_d_q7, avg_d_q8, avg_d_q9,finland['avg_d_mbps'].max()]
labels = ['<{}'.format(avg_d_q1),
        '>={} & <{}'.format(avg_d_q1,avg_d_q2),
        '>={} & <{}'.format(avg_d_q2,avg_d_q3),
        '>={} & <{}'.format(avg_d_q3,avg_d_q4),
        '>={} & <{}'.format(avg_d_q4,avg_d_q5),
        '>={} & <{}'.format(avg_d_q5,avg_d_q6),
        '>={} & <{}'.format(avg_d_q6,avg_d_q7),
        '>={} & <{}'.format(avg_d_q7,avg_d_q8),
        '>={} & <{}'.format(avg_d_q8,avg_d_q9),
        '>={}'.format(avg_d_q9)
]

finland['avg_d_mbps_ranges'] = pd.cut(finland['avg_d_mbps'], bins=bins, labels=labels)

finland = finland.sort_values(by=['avg_d_mbps'])

#print(finland['avg_d_mbps_ranges'].unique())



fig = px.choropleth_mapbox(finland,
                geojson=finland.geometry,
                locations=finland.index,
                color="avg_d_mbps_ranges",
                color_discrete_sequence= px.colors.sequential.Turbo_r,
                opacity=0.5,
                hover_data = ['avg_d_mbps_ranges','avg_d_mbps','avg_u_kbps','tests','devices'],
                custom_data = ['avg_d_mbps'],
                center = {'lat':60.2825,'lon':24.9271},
                mapbox_style="open-street-map")
#fig.update_geos(fitbounds="locations", visible=False)
#fig.show()


app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
app.layout = html.Div([
    html.H1('Speedtest by Ookla Mobile Network'),
    html.H2('Performance Map Tiles'),
    dcc.Markdown('''
                #### This dashbord was built using [Ookla Open Dataset](https://registry.opendata.aws/speedtest-global-performance/).
                ##### Used data shows mobile (cellular) network performance metrics in zoom level 16 web mercator tiles (approximately 610.8 meters by 610.8 meters at the equator).
            '''),

    dcc.Graph(id='map',figure=fig),
    html.Div([
        html.H3(id='counter')
    ],style={'display':'inline-block'})
])


@app.callback(Output('counter', 'children'),
              [Input('map', 'hoverData')])
def find_counter(hoverData):
    #pts = len(selectedData['points'])
    #rng_or_lp = list(selectedData.keys())
    #rng_or_lp.remove('lassoPoints')
    mean = hoverData['points'][0]['customdata'][0]
    #print(mean)
   # data = selectedData['points']['customdata'[2]]
    #rng_or_lp = list(selectedData.keys())
    #rng_or_lp.remove('points')
    #avg_thp = mean(selectedData[rng_or_lp[0]]['customdata'[1]])
    #return 'Counter = {:.2f}'.format(mean)
    return 'Avg_d_mbps in the tile you hover over is {} Mpbs'.format(mean)

if __name__ == '__main__':
    app.run_server()  # Turn off reloader if inside Jupyter
