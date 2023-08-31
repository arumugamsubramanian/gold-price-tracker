import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Create the "dashboard" directory if it doesn't exist
if not os.path.exists('dashboard'):
    os.makedirs('dashboard')

# Load CSV data
data = pd.read_csv('gold_prices.csv')

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Calculate price differences per day for each metal type
data['Price Diff'] = data.groupby('Type')['Price'].diff()

# Create a line chart for price differences per day
fig_line = px.line(data, x='Date', y='Price Diff', color='Type',
                   title='Metal Price Differences per Day')

# Create a bar chart for average prices per metal type
avg_prices = data.groupby('Type')['Price'].mean().reset_index()
fig_bar = px.bar(avg_prices, x='Type', y='Price', color='Type',
                 title='Average Metal Prices')

# Create a scatter plot for metal prices over time
fig_scatter = px.scatter(data, x='Date', y='Price', color='Type',
                         title='Metal Prices Over Time')

# Create a tabular column chart of the price list
fig_table = go.Figure(data=[go.Table(
    header=dict(values=['Date', 'Type', 'Price']),
    cells=dict(values=[data['Date'], data['Type'], data['Price']])),
])
fig_table.update_layout(title_text='Metal Price List')

# Save the plots to an HTML file
with open('dashboard/index.html', 'w') as f:
    f.write('<h1 style="text-align: center;">Metal Price Dashboard</h1>')
    f.write(fig_line.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_bar.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_scatter.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_table.to_html(full_html=False, include_plotlyjs='cdn'))
