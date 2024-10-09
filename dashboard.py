import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Manually provide the file path to the dataset
data = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Automatically sample 3001 rows
mySample = data.sample(n=3001, random_state=55047)

# Dropdown filters
selected_product = st.selectbox('Select Product:', mySample['Product'].unique())
selected_category = st.selectbox('Select Category:', mySample['Category'].unique())
selected_import_export = st.selectbox('Select Import/Export:', mySample['Import_Export'].unique())

# Filter the sample based on the selections
filtered_sample = mySample[
    (mySample['Product'] == selected_product) &
    (mySample['Category'] == selected_category) &
    (mySample['Import_Export'] == selected_import_export)
]

# Create columns for side-by-side visualization
col1, col2 = st.columns(2)

# Graph 1: Scatter plot of Quantity vs Value
with col1:
    fig_scatter = px.scatter(filtered_sample, x='Quantity', y='Value', title='Scatter Plot of Quantity vs Value')
    fig_scatter.update_layout(xaxis_title='Quantity', yaxis_title='Value')
    st.plotly_chart(fig_scatter)

# Graph 2: Boxplot for Value based on Product
with col2:
    fig_boxplot = px.box(filtered_sample, x='Product', y='Value', title=f'Boxplot of Value for {selected_product}')
    fig_boxplot.update_layout(xaxis_title='Product', yaxis_title='Value')
    st.plotly_chart(fig_boxplot)

# Second row of two more graphs
col3, col4 = st.columns(2)

# Graph 3: Pie plot for Payment Terms
with col3:
    payment_terms_count = filtered_sample['Payment_Terms'].value_counts()
    labels = payment_terms_count.index.tolist()
    values = payment_terms_count.values.tolist()
    
    fig_pie = px.pie(values=values, names=labels, title='Pie Plot of Payment Terms', 
                     hole=0.3, labels={'values': 'Count', 'names': 'Payment Terms'})
    st.plotly_chart(fig_pie)

# Graph 4: Histogram of Value
with col4:
    fig_histogram = px.histogram(filtered_sample, x='Value', nbins=20, title='Histogram of Transaction Values', 
                                  color_discrete_sequence=['yellow'])
    fig_histogram.update_layout(xaxis_title='Value', yaxis_title='Frequency')
    st.plotly_chart(fig_histogram)
    
# Third row: 3D scatter plot
fig_3d = px.scatter_3d(
    filtered_sample.groupby(['Import_Export', 'Category']).size().reset_index(name='Count'),
    x='Import_Export', y='Category', z='Count',
    color='Import_Export', title='3D Scatter: Category-wise Imports/Exports',
    size_max=20
)
st.plotly_chart(fig_3d)
