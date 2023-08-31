import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load CSV data
data = pd.read_csv('gold_prices.csv')

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Group by Date and Type, and calculate the mean price
agg_data = data.groupby(['Date', 'Type'])['Price'].mean().reset_index()

# Create a line chart for price differences per day
fig_line = px.line(agg_data, x='Date', y='Price', color='Type',
                   title='Metal Price Differences per Day')

# Create a bar chart for average prices per metal type
fig_bar = px.bar(agg_data.groupby('Type')['Price'].mean().reset_index(),
                 x='Type', y='Price', color='Type',
                 title='Average Metal Prices')

# Create a scatter plot for metal prices over time
fig_scatter = px.scatter(agg_data, x='Date', y='Price', color='Type',
                         title='Metal Prices Over Time')

# Create a tabular column chart of the price list
fig_table = go.Figure(data=[go.Table(
    header=dict(values=['Date', 'Type', 'Price']),
    cells=dict(values=[agg_data['Date'], agg_data['Type'], agg_data['Price']])),
])
fig_table.update_layout(title_text='Metal Price List')

# Save the plots to an HTML file
with open('dashboard.html', 'w') as f:
    f.write('<h1 style="text-align: center;">Metal Price Dashboard</h1>')
    f.write(fig_line.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_bar.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_scatter.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_table.to_html(full_html=False, include_plotlyjs='cdn'))
