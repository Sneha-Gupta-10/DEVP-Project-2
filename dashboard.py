import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Manually provide the file path to the dataset
data = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Automatically sample 3001 rows
mySample = data.sample(n=3001, random_state=55047)

# Sidebar filters
shipping_methods = ["All"] + mySample['Shipping_Method'].unique().tolist()
categories = ["All"] + mySample['Category'].unique().tolist()
import_export_options = ["All"] + mySample['Import_Export'].unique().tolist()

selected_shipping_method = st.sidebar.selectbox('Select Shipping Method:', shipping_methods)
selected_category = st.sidebar.selectbox('Select Category:', categories)
selected_import_export = st.sidebar.selectbox('Select Import/Export:', import_export_options)

# Apply the filters, and if 'All' is selected, ignore that filter
filtered_sample = mySample.copy()

if selected_shipping_method != "All":
    filtered_sample = filtered_sample[filtered_sample['Shipping_Method'] == selected_shipping_method]

if selected_category != "All":
    filtered_sample = filtered_sample[filtered_sample['Category'] == selected_category]

if selected_import_export != "All":
    filtered_sample = filtered_sample[filtered_sample['Import_Export'] == selected_import_export]

# Create columns for side-by-side visualization
col1, col2 = st.columns(2)

# Graph 1: Boxplot for Value based on Shipping Method
with col1:
    fig_boxplot = px.box(filtered_sample, x='Shipping_Method', y='Value', title=f'Boxplot of Value by Shipping Method')
    fig_boxplot.update_layout(xaxis_title='Shipping Method', yaxis_title='Value')
    st.plotly_chart(fig_boxplot)

# Graph 2: Pie plot for Payment Terms
with col2:
    payment_terms_count = filtered_sample['Payment_Terms'].value_counts()
    labels = payment_terms_count.index.tolist()
    values = payment_terms_count.values.tolist()
    
    fig_pie = px.pie(values=values, names=labels, title='Pie Plot of Payment Terms', 
                     hole=0.3, labels={'values': 'Count', 'names': 'Payment Terms'})
    st.plotly_chart(fig_pie)

# Second row of two more graphs
col3, col4 = st.columns(2)

# Graph 3: Histogram of Value
with col3:
    fig_histogram = px.histogram(filtered_sample, x='Value', nbins=20, title='Histogram of Transaction Values', 
                                  color_discrete_sequence=['yellow'])
    fig_histogram.update_layout(xaxis_title='Value', yaxis_title='Frequency')
    st.plotly_chart(fig_histogram)

# Graph 4: 3D scatter plot
with col4:
    fig_3d = px.scatter_3d(
        filtered_sample.groupby(['Import_Export', 'Category']).size().reset_index(name='Count'),
        x='Import_Export', y='Category', z='Count',
        color='Import_Export', title='3D Scatter: Category-wise Imports/Exports',
        size_max=20
    )
    st.plotly_chart(fig_3d)
