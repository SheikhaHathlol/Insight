import pandas as pd 
import streamlit as st
import requests
from secret import gemini_key

# Basic analysis function:    
def basic_analysis(df):   
    analysis = {
        "summary": df.describe().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.to_dict(),
        "Duplicated rows": df.duplicated().sum(),
        "distinct_values": df.apply(pd.Series.unique).to_dict()
    }
    
    df_sample = df.sample(10).to_dict()
    return {"Basic_Analysis": analysis ,"Sample_Data": df_sample}


# Columns Analysis:
def columns_analysis(df):
    column_analysis = {}

    for col in df.columns:
        col_data = {}  
        
        # 1 (numerical or categorical)
        if df[col].dtype == 'object':
            col_data['data_type'] = 'cate'  
        else:
            col_data['data_type'] = 'num'   

        # 2 distinct values 
        if col_data['data_type'] == 'cate':
            # categorical columns: top 5 frequent values and the total number of distinct values
            top_frequent = df[col].value_counts().head(5).to_dict()
            total_distinct_values = df[col].nunique()  # Total number of distinct values
            col_data['distinct_values'] = {
                'top_5_frequent': top_frequent,
                'total_distinct_values': total_distinct_values
            }
        else:
            # numerical columns: the distribution 
            distribution = df[col].describe().to_dict()
            col_data['distribution'] = distribution

        # 3 missing values Count
        missing_values = df[col].isnull().sum()
        col_data['missing_values'] = missing_values

        # 4 duplicated values count
        duplicated_values = df[col].duplicated().sum()
        col_data['duplicated_values'] = duplicated_values

        # 5 trailing whitespace (categorical columns)
        if col_data['data_type'] == 'cate':
            whitespace = df[col].str.strip().nunique() != df[col].nunique()
            col_data['trailing_whitespace'] = whitespace

        #6 date/time Consistency (if the column has dates)
        if df[col].dtype == 'datetime64[ns]':
            min_date = df[col].min()
            max_date = df[col].max()
            col_data['date_range'] = (min_date, max_date)
            
        #7 range violations (for numerical columns)
        if col_data['data_type'] == 'num':
            outliers = (df[col] < df[col].quantile(0.05)) | (df[col] > df[col].quantile(0.95))
            col_data['range_violations'] = outliers.sum()

        # 8 store all column data
        column_analysis[col] = col_data
        
    return column_analysis

# check for duplicate or redundant Columns 
def check_duplicate_columns(df):
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()
    return duplicate_columns

def columns_description(df):
    # calling functions to get the analysis results
    column_data = columns_analysis(df)
    duplicate_columns = check_duplicate_columns(df)

    # Saving the result in a list to pass it to the API 
    columns_description = []

    for col, analysis in column_data.items():
        columns_description.append(f"Column: {col}")
        for key, value in analysis.items():
            columns_description.append(f"  {key}: {value}")
        columns_description.append("") 
    return {"columns_description": columns_description, "duplicated_columns": duplicate_columns}

# query 
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
headers = {
    "Content-Type": "application/json"
}

def query_with_gemini(prompt, task):
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    

def visualize_data(dataframe, column_name):
    col_data = dataframe[column_name]
    
    # For numeric columns, display a histogram and boxplot
    if pd.api.types.is_numeric_dtype(col_data):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(col_data, kde=True, ax=ax)
        ax.set_title(f"Histogram of {column_name}")
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x=col_data, ax=ax)
        ax.set_title(f"Boxplot of {column_name}")
        st.pyplot(fig)
    
    # For categorical columns, display a bar chart or pie chart
    elif pd.api.types.is_categorical_dtype(col_data) or col_data.dtype == 'object':
        fig, ax = plt.subplots(figsize=(6, 4))
        col_data.value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f"Bar chart of {column_name}")
        st.pyplot(fig)
        
    # For temporal data, plot trends over time
    elif pd.api.types.is_datetime64_any_dtype(col_data):
        col_data = col_data.dt.to_period('M')  # Group by month (you can adjust)
        fig, ax = plt.subplots(figsize=(6, 4))
        col_data.value_counts().sort_index().plot(kind='line', ax=ax)
        ax.set_title(f"Trends in {column_name} over Time")
        st.pyplot(fig)
        
        
    
def analyze_column(dataframe, column_name):
    col_data = dataframe[column_name]
    
    # If the column is numeric
    
    if pd.api.types.is_numeric_dtype(col_data):
        prompt = f"""
        Please analyze the column selected by the user using descriptive analysis. The column contains the following data: {col_data.sample(10).to_list()}. 
        First, determine the type of data in the column (numerical, categorical, or temporal), and perform the following analysis based on the type of data:

        1. If the column contains numerical data:
            - Calculate the following descriptive statistics:
              - Mean (average)
              - Median
              - Minimum value (Min)
              - Maximum value (Max)
              - Standard Deviation
            - Display a histogram and boxplot of the data to visualize the distribution.
            - Identify any outliers if they exist (for example, values significantly higher or lower than the rest of the data).
        """
    
    # If the column is categorical
    elif pd.api.types.is_categorical_dtype(col_data) or col_data.dtype == 'object':
        prompt = f"""
        Please analyze the column selected by the user using descriptive analysis. The column contains the following data: {col_data.sample(10).to_list()}. 
        First, determine the type of data in the column (numerical, categorical, or temporal), and perform the following analysis based on the type of data:

        2. If the column contains categorical data:
            - Calculate the frequency and percentage for each category in the column.
            - Display a pie chart or bar chart to visualize the distribution of the categories.
        """
    
    # If the column contains temporal data
    elif pd.api.types.is_datetime64_any_dtype(col_data):
        prompt = f"""
        Please analyze the column selected by the user using descriptive analysis. The column contains the following data: {col_data.sample(10).to_list()}. 
        First, determine the type of data in the column (numerical, categorical, or temporal), and perform the following analysis based on the type of data:

        3. If the column contains temporal data (dates/times):
            - Analyze the trends or changes over time.
            - Display a line chart to show how the values change over time.
            - Provide insights into any noticeable trends or patterns (e.g., seasonality, peaks).
        """
    
    else:
        return "Unknown column type for analysis."
    
    # Send the prompt to Gemini API
    return query_with_gemini(prompt, "data analysis")