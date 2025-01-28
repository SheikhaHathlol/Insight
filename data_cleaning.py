import pandas as pd 
import streamlit as st 
import requests
from secret import api_key

# we should add a valdiation function for the file type.
uploaded_file = st.file_uploader("Upload your data file (CSV or Excel)",type=["csv","xlsx"])

# this code will be converted into a function. 
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display data:
    st.write("Uploaded data: ")
    st.write(df)

    # Basic analysis:
    st.write("Basic Analysis: ")
    st.write(df.describe())

    # Missing Values:
    if df.isnull().any().any():
        st.write("Missing values in the dataset: ")
        st.write(df.isnull().sum())
    

# Basic analysis function:
def analyze_data(df):
    analysis = {
        "summary" : df.describe().to_dict(),
        "missing_values" : df.isnull().sum().to_dict(),
        "data_types" : df.dtypes.astype(str).to_dict(),
        "Duplicated rows": df.duplicated().sum(),
        "outliers" : "Custom logic to detect oultiers"
    }
    
    return analysis

# now we are going to use the AI to give us summarization about the dataset and we're going to enter the analysis dic as a prompt 
def query_deepseek(analysis):
    key = api_key
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    query = {
        "model" :"deepseek-reasoner",
        "messages": [
            {"role": "user", "content": f"Here is the data analysis: {analysis}. Provide a summary and suggestions for cleaning the data."}
        ],
        "temperature":  0.7,
        "max_tokens" : 300
        
    }
        
    st.write("Debugging: Query being sent to DeepSeek API:")
    st.write(query)
    
    
    headers = {
        f"Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    

    response = requests.post(api_url,json=query,headers = headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"
    
    

if uploaded_file is not None:
    analysis = analyze_data(df)
    st.write("Analysis Result:")
    st.write(analysis)
    
    deepseek_response = query_deepseek(analysis)
    st.write("DeepSeek Suggestions:")
    st.write(deepseek_response)

