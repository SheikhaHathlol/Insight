import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt


st.title("Welcome to Insight!")

#upload a file 
uploaded_file = st.file_uploader("Choose a file")

# Data Cleaning 
if uploaded_file is not None: 
    dataframe = pd.read_excel(uploaded_file) 
    st.write("Dataset:")
    st.write(dataframe)
    
    # Check for Missing Values:
    st.write("Missing values in each column:")
    st.write(dataframe.isnull().sum())
    
    # Duplicate Entries: 
    st.write("Duplicate Entries")
    du_col = dataframe.apply(lambda x: x.duplicated().sum())
    table_dup = pd.DataFrame(du_col, columns=['Duplicated Count'])
    st.write(table_dup)
    
    # Column Type:
    st.write("Column Type") 
    st.write(pd.DataFrame(dataframe.dtypes, columns=["Column Type"]))
    
    