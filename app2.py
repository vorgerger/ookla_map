import geopandas
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import Input, Output

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
#print(finland['avg_d_mbps_ranges'].unique())

#finland = finland.head(1000)

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
#USERNAME_PASSWORD_PAIRS = [['XXXX', 'XXXX']]
#auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
#server = app.server
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
    mean = hoverData['points'][0]['customdata'][0]
    return 'Avg_d_mbps in the tile you hover over is {} Mpbs.'.format(mean)

if __name__ == '__main__':
    app.run_server()  # Turn off reloader if inside Jupyter
