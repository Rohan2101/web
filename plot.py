import pandas as pd
import plotly.express as px

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
# Aggregate counts for each cancer type
cancer_counts = df.groupby('Cancer group/site')['Count'].sum()

# Sort cancers by counts and select the 2nd to 8th items
selected_cancers = cancer_counts.sort_values(ascending=False).index[1:8]

# Filter the DataFrame to include only the selected cancers
df_selected = df[df['Cancer group/site'].isin(selected_cancers)]

# Grouping data by 'Cancer group/site' and 'Age group (years)', and summing up the counts
grouped_data = df_selected.groupby(['Cancer group/site', 'Age group (years)'])['Count'].sum().unstack()

# Resetting index to make 'Cancer group/site' a regular column
grouped_data = grouped_data.reset_index()

# Melt the DataFrame to make it suitable for Plotly
melted_data = pd.melt(grouped_data, id_vars='Cancer group/site', var_name='Age group (years)', value_name='Count')

# Plotting with Plotly Express
fig = px.bar(melted_data, x='Cancer group/site', y='Count', color='Age group (years)',
             title='Cancer Types by Age Group', 
             labels={'Cancer group/site': 'Cancer Types', 'Count': 'Count', 'Age group (years)': 'Age group (years)'},
             barmode='stack')

# Rotate x-axis labels for better readability
fig.update_layout(xaxis_tickangle=-45)

# Show the plot
fig.show()
