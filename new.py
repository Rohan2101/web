from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10
from bokeh.io import output_notebook
from bokeh.io import output_file
import pandas as pd

df = pd.read_excel("aihw-can-122-CDiA-2023-Book-1a-Cancer-incidence-age-standardised-rates-5-year-age-groups.xlsx",sheet_name=1,header=5)

df = df[df['Age group (years)'] != 'All ages combined']

age_map = {
    '00–04': '0-19',
    '05–09': '0-19',
    '10–14': '0-19',
    '15–19': '0-19',
    '20–24': '20-39',
    '25–29': '20-39',
    '30–34': '20-39',
    '35–39': '20-39',
    '40–44': '40-59',
    '45–49': '40-59',
    '50–54': '40-59',
    '55–59': '40-59',
    '60–64': '60-79',
    '65–69': '60-79',
    '70–74': '60-79',
    '75–79': '60-79',
    '80–84': '80+',
    '85–89': '80+',
    '90+': '80+'
}

df['Age group (years)'] = df['Age group (years)'].replace(age_map)

df = df[df['Sex'] != 'Persons']

# Sample data (replace this with your actual DataFrame)
# Create DataFrame
data = df

# Group by 'Age group (years)' and 'Sex' and count the occurrences
grouped_data = df.groupby(['Age group (years)', 'Sex']).size().reset_index(name='count')

# Convert data to ColumnDataSource
source = ColumnDataSource(grouped_data)

# Bokeh plot
p = figure(x_range=grouped_data['Age group (years)'].unique(), height=350, title="Counts by Age Group and Sex",
           toolbar_location=None, tools="")

# Plot bars
p.vbar(x=dodge('Age group (years)', -0.2, range=p.x_range), top='count', width=0.4, source=source,
       color=factor_cmap('Sex',palette=('#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff'), factors=grouped_data['Sex'].unique()), legend_field='Sex')

# Add labels and legend
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.axis_label = "Age group (years)"
p.yaxis.axis_label = "Count"
p.title.text_font_size = "16px"
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

# Show the plot
output_file('hist.html')
show(p)
