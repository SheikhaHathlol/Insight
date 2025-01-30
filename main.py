import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
from data_cleaning import data_cleaning
from data_description import data_description
from helpers import query_with_gemini,visualize_data, analyze_column
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from pygwalker.api.streamlit import StreamlitRenderer
from secret import gemini_key

# UI
st.set_page_config(page_title="Data Analysis", layout="wide")

st.sidebar.title("📂 Main Menu")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("📤 Upload"):
    st.session_state.page = "Upload"

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    st.title("🏠 Home")
    st.write("### Insight is an AI-powered data analysis platform designed to help both technical and non-technical users analyze their data quickly and effectively.")

elif st.session_state.page == "Upload":
    st.title("📤 Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            dataframe = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            dataframe = pd.read_excel(uploaded_file, engine="openpyxl")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Data Description", "🧹 Data Cleaning", "📊 Data Analysis", "📉 Data Visualization"
        ])

        with tab1:
            st.subheader("📄 Data Description")
            prompt = data_description(dataframe)
            description = query_with_gemini(prompt, "data description")
            st.write(description)

        with tab2:
            st.subheader("🧹 Data Cleaning Suggestions")
            prompt = data_cleaning(dataframe) 
            cleaning_suggestions = query_with_gemini(prompt, "data cleaning")
            st.write(cleaning_suggestions)

        with tab3:
            st.subheader("📊 Data Analysis")
            selected_columns = st.multiselect("Choose columns for analysis:", list(dataframe.columns))
            if selected_columns:
                for column in selected_columns:
                    st.write(f"### Analyzing column: {column}")
                    st.write(analyze_column(dataframe, column))
                    visualize_data(dataframe, column)

        with tab4:
            st.subheader("📉 Data Visualization")
            pyg_app = StreamlitRenderer(dataframe)
            pyg_app.explorer()