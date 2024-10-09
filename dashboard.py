import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Manually provide the file path to the dataset
data = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Automatically sample 3001 rows without needing a button click
mySample = data.sample(n=3001, random_state=55047)

# Extract and display non-categorical columns
non_categorical_columns = ['Quantity', 'Value', 'Customs_Code', 'Weight']
if all(col in mySample.columns for col in non_categorical_columns):
    non_categorical_df = mySample[non_categorical_columns]

    # Scatter plot of Quantity vs Value
    fig_scatter = px.scatter(mySample, x='Quantity', y='Value', title='Scatter Plot of Quantity vs Value')
    fig_scatter.update_layout(xaxis_title='Quantity', yaxis_title='Value')
    st.plotly_chart(fig_scatter)  # Display the scatter plot

    # Histogram with Density Curve for the 'Quantity' column
    density_quantity = ff.create_distplot([non_categorical_df['Quantity']], ['Density'], 
                                           show_hist=True, colors=['blue'], 
                                           bin_size=5)
    density_quantity.update_layout(title='Distribution with Density Curve for Quantity',
                                   xaxis_title='Data Values',
                                   yaxis_title='Frequency')
    st.plotly_chart(density_quantity)  # Display the histogram with density curve

    # Histogram with Density Curve for the 'Weight' column
    density_weight = ff.create_distplot([non_categorical_df['Weight']], ['Density'], 
                                         show_hist=True, colors=['red'], 
                                         bin_size=5)
    density_weight.update_layout(title='Distribution with Density Curve for Weight',
                                 xaxis_title='Data Values',
                                 yaxis_title='Frequency')
    st.plotly_chart(density_weight)  # Display the histogram with density curve

    # Histogram with Density Curve for the 'Value' column
    density_value = ff.create_distplot([non_categorical_df['Value']], ['Density'], 
                                        show_hist=True, colors=['purple'], 
                                        bin_size=5)
    density_value.update_layout(title='Distribution with Density Curve for Value',
                                xaxis_title='Data Values',
                                yaxis_title='Frequency')
    st.plotly_chart(density_value)  # Display the histogram with density curve

# Extract and display categorical columns
categorical_variables = ["Country", "Product", "Import_Export", "Category", "Port", "Shipping_Method", "Supplier", "Customer", "Payment_Terms"]

if all(col in mySample.columns for col in categorical_variables):
    # Get the top 10 categories by frequency
    top_10_categories = mySample['Product'].value_counts().nlargest(10).index
    
    # Filtering the DataFrame to only include the top 10 categories
    top_10_sample = mySample[mySample['Product'].isin(top_10_categories)]

    # Create a boxplot for Value based on top 10 product categories
    fig_boxplot = px.box(top_10_sample, x='Product', y='Value', title='Boxplot of Value by Top 10 Products')
    fig_boxplot.update_layout(xaxis_title='Product', yaxis_title='Value')
    st.plotly_chart(fig_boxplot)  # Display the Plotly boxplot

    # Count payment terms
    payment_terms_count = mySample['Payment_Terms'].value_counts()

    # Data for pie plot
    labels = payment_terms_count.index.tolist()
    values = payment_terms_count.values.tolist()

    # Creating pie plot with percentage labels
    fig_pie = px.pie(values=values, names=labels, title='Pie Plot of Payment Terms', 
                     labels={'values': 'Count', 'names': 'Payment Terms'},
                     hole=0.3)  # Adding a donut chart for better aesthetics
    st.plotly_chart(fig_pie)  # Display the pie chart

    # Histogram of the 'Value' column
    fig_histogram = px.histogram(mySample, x='Value', nbins=20, title='Histogram of Transaction Values', 
                                  color_discrete_sequence=['yellow'])
    fig_histogram.update_layout(xaxis_title='Value', yaxis_title='Frequency')
    st.plotly_chart(fig_histogram)  # Display the histogram

    # Group by Import_Export and Category and calculate the count
    count_data = mySample.groupby(['Import_Export', 'Category']).size().reset_index(name='Count')

    # Create animated 3D scatter plot
    Area_distribution_3d_plot = px.scatter_3d(
        count_data, 
        x='Import_Export', 
        y='Category', 
        z='Count',
        color='Import_Export',
        title='Category-wise Imports and Exports',
        size_max=20,
        animation_frame='Count',  # Note: The animation may not work as expected with the current setup
    )

    # Set the duration of each frame
    Area_distribution_3d_plot.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100

    # Show the 3D plot
    st.plotly_chart(Area_distribution_3d_plot)  # Display the animated 3D plot

else:
    st.write("Some of the specified categorical columns are not in the dataset.")
