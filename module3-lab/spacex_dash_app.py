# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

unique_launch_sites = list(set(spacex_df["Launch Site"]))
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for i in range(len(unique_launch_sites)):
    dropdown_options.append({'label': unique_launch_sites[i], 'value': unique_launch_sites[i]})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                style={'textAlign': 'center', 'color': '#503D36',
                                        'font-size': 40}),
                        # TASK 1: Add a dropdown list to enable Launch Site selection
                        # The default select value is for ALL sites
                        # dcc.Dropdown(id='site-dropdown',...)
                        html.Br(),
                        dcc.Dropdown(id="site-dropdown-menu", value="ALL", placeholder="Select a Launch Site here", searchable=True, options=dropdown_options),

                        # TASK 2: Add a pie chart to show the total successful launches count for all sites
                        # If a specific launch site was selected, show the Success vs. Failed counts for the site
                        html.Div(dcc.Graph(id='success-pie-chart')),
                        html.Br(),

                        html.P("Payload range (Kg):"),
                        # TASK 3: Add a slider to select payload range
                        dcc.RangeSlider(id='payload-slider',
                            min=0, max=10000, step=1000,
                            marks={0: '0',
                                100: '100'},
                            value=[min_payload, max_payload]),

                        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                        ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown-menu', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
            names='Launch Site',
            title="Success rate of all sites")
        return fig
    else:
        site_data = spacex_df[spacex_df["Launch Site"] == entered_site]
        class_counts = site_data['class'].value_counts()
        fig = px.pie(values=class_counts, names=class_counts.index, title=f"Success rate of {entered_site}")
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown-menu', component_property='value'),
            Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_values):
    min_payload, max_payload = payload_values[0], payload_values[1]
    print(min_payload, max_payload)
    print("REACHES HERE")
    if entered_site == 'ALL':
        df_payload_mass = spacex_df["Payload Mass (kg)"]
        df_class = spacex_df["class"]
        fig = px.scatter(x=df_payload_mass, y=df_class, color=spacex_df["Booster Version Category"])
        return fig
    else:
        df_payload_mass = spacex_df["Payload Mass (kg)"]
        df_class = spacex_df["class"]
        fig = px.scatter(x=df_payload_mass, y=df_class, color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
