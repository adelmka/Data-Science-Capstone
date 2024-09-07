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

# Define the Dash app
app = dash.Dash(__name__)

# Create a list of unique launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Add an 'All Sites' option
launch_sites_options = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites_options += [{'label': site, 'value': site} for site in launch_sites]

# Define the app layout
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Launch site dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites_options,
                 placeholder='Select a Launch Site',
                 searchable=True,
                 value='ALL'),  # Default value
    
    # Placeholder for other components
    html.Div(id='output-container')
])

# Add a placeholder for the pie chart in the layout
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Launch site dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites_options,
                 placeholder='Select a Launch Site',
                 searchable=True,
                 value='ALL'),  # Default value
    
    # Pie chart
    dcc.Graph(id='success-pie-chart'),
    
    # Placeholder for other components
    html.Div(id='output-container')
])

# Callback function to update the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Aggregate data for all sites
        success_counts = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        title = 'Total Successful Launches by Site'
        fig = px.pie(success_counts, 
                     names='Launch Site', 
                     values='class', 
                     title=title)
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts()
        title = f'Total Success Launches for site {selected_site}'
        fig = px.pie(success_counts, 
                     names=success_counts.index, 
                     values=success_counts.values, 
                     title=title)
    
    return fig

# Update the app layout to include the range slider
# Update the app layout to include the range slider below the pie chart
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Launch site dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites_options,
                 placeholder='Select a Launch Site',
                 searchable=True,
                 value='ALL'),  # Default value
    
    # Pie chart
    dcc.Graph(id='success-pie-chart'),
    
    # Payload range slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: f'{i} kg' for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),  # Default range
    
    # Placeholder for other components
    html.Div(id='output-container')
])

# Callback function to update the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter data based on the selected payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        # Plot all sites
        title = 'Correlation between Payload and Success for All Sites'
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=title,
                         hover_data=['Launch Site'])
    else:
        # Filter data for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        title = f'Correlation between Payload and Success for site {selected_site}'
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=title)
    
    return fig

# Update the app layout to include the scatter plot
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Launch site dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites_options,
                 placeholder='Select a Launch Site',
                 searchable=True,
                 value='ALL'),  # Default value
    
    # Pie chart
    dcc.Graph(id='success-pie-chart'),
    
    # Payload range slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: f'{i} kg' for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),  # Default range
    
    # Scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# Run the app
if __name__ == '__main__':
    app.run_server()