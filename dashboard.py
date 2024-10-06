import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

# File uploader to allow users to upload a CSV file
uploaded_file = st.file_uploader("Imports_Exports_Dataset", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Dataset loaded successfully!")
    st.dataframe(data.head())  # Display the first few rows of the dataset

    # Button to trigger sampling
    if st.button('Sample 3001 Rows'):
        mySample = data.sample(n=3001, random_state=55047)
        st.write("Sampled 3001 rows:")
        st.dataframe(mySample.head())  # Display first few rows of the sampled data

        # Display the shape of the sampled data
        st.write("Shape of the sampled data:")
        st.write(mySample.shape)  # Display (rows, columns) of the sampled DataFrame

        # Display the columns of the sampled data
        st.write("Columns in the sampled data:")
        st.write(mySample.columns.tolist())  # Display column names

        # Extract and display non-categorical columns
        non_categorical_columns = ['Quantity', 'Value', 'Customs_Code', 'Weight']
        if all(col in mySample.columns for col in non_categorical_columns):
            non_categorical_df = mySample[non_categorical_columns]
            st.write("Non-categorical columns dataframe:")
            st.dataframe(non_categorical_df)

            # Descriptive Statistics of the Non-Categorical Set
            non_categorical_stats = non_categorical_df.describe()
            non_categorical_stats = np.round(non_categorical_stats, 2)
            st.write("Descriptive statistics of non-categorical columns:")
            st.dataframe(non_categorical_stats)
        else:
            st.write("Some of the specified columns are not in the dataset.")

        # Extract and display categorical columns
        categorical_variables = ["Country", "Product", "Import_Export", "Category", "Port", "Shipping_Method", "Supplier", "Customer", "Payment_Terms"]

        if all(col in mySample.columns for col in categorical_variables):
            categ = mySample[categorical_variables]
            st.write("Categorical columns dataframe:")
            st.dataframe(categ)  # Display the categorical data

            # Display value counts for the "Category" column
            category_counts = pd.DataFrame(mySample["Category"].value_counts()).reset_index()
            category_counts.columns = ['Category', 'Count']  # Rename columns for clarity
            st.write("Value counts of the 'Category' column:")
            st.dataframe(category_counts)  # Display the value counts DataFrame

            # Get the top 10 categories by frequency
            top_10_categories = mySample['Product'].value_counts().nlargest(10).index
            
            # Filtering the DataFrame to only include the top 10 categories
            top_10_sample = mySample[mySample['Product'].isin(top_10_categories)]

            # Create a boxplot for Value based on top 10 product categories
            fig_boxplot = px.box(top_10_sample, x='Product', y='Value', title='Boxplot of Value by Top 10 Products')
            fig_boxplot.update_layout(xaxis_title='Product', yaxis_title='Value')
            st.plotly_chart(fig_boxplot)  # Display the Plotly boxplot

            # Scatter plot of Quantity vs Value
            fig_scatter = px.scatter(mySample, x='Quantity', y='Value', title='Scatter Plot of Quantity vs Value')
            fig_scatter.update_layout(xaxis_title='Quantity', yaxis_title='Value')
            st.plotly_chart(fig_scatter)  # Display the scatter plot

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
else:
    st.write("Please upload a CSV file to proceed.")
