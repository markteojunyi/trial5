import streamlit as st
import pandas as pd
# from helper_function.stpassword import check_password  

# if not check_password():  
#     st.stop()

# Show a spinner until the page is fully loaded
with st.spinner('Loading the application, we ask for your patience...'):

    # Title of the app
    st.title('Prices of resale flats')

    # Load the CSV file automatically (ensure the path is correct)
    csv_file_path = 'resalepricesfrom2017.csv' 

    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Add some basic filters for the data
    st.subheader('Filter your data to get the info that you need')

    # Get all column names in the DataFrame
    columns = df.columns.tolist()

    # Let the user select the column to filter
    selected_columns = st.multiselect('Select any number of criteria to filter', columns)

    # Initialize an empty DataFrame for filtered results
    filtered_data = df

    # Apply filters for the selected columns
    for selected_column in selected_columns:
        unique_values = df[selected_column].unique()
        selected_values = st.multiselect(f'Filter by {selected_column}', unique_values)

        # Apply filter only if values are selected
        if selected_values:
            filtered_data = filtered_data[filtered_data[selected_column].isin(selected_values)]

    # Display the filtered data
    st.subheader('Filtered Data')
    if not filtered_data.empty:
        st.write(filtered_data)
    else:
        st.write('No data available for the selected filters.')

    # st.write(" ")

    # # Show the raw data in a table
    # st.subheader('Entire raw data of all resale flats from 2017 onwards')
    # st.write(df)
