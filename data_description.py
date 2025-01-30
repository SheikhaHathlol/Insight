import pandas as pd 
import streamlit as st 
import google.generativeai as genai
from secret import gemini_key

# first,Data description (will convert the steps below into a function so that we can call it from the main file)
user_description = st.text_input("Enter dataset description") # optional 
uploaded_file = st.file_uploader("Upload your data file (CSV or Excel)",type=["csv","xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    def analyze_data(df):
        analysis = {
            "summary" : df.describe().to_dict(),
            "missing_values" : df.isnull().sum().to_dict(),
            "Data_types" : df.dtypes.to_dict(),
            "Duplicated rows": df.duplicated().sum(),
            "Distinct_values": df.value_counts().to_dict(),
            "User_discription": user_description if user_description is not None else "No description provided"} 
        return analysis

    analysis = analyze_data(df)
    df_sample = df.sample(10)
    # AI model: 
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    desc_response = model.generate_content(
        f"""Please generate a detailed description of the following dataset: dataset sample:{df_sample}. summary: {analysis}.The description should include:

        1- Title and Overview: Provide a 2-sentence general description of the dataset.
        2- Count of Values: Indicate how many rows are present in the dataset.
        3- Columns: List each column and describe its contents in 2-4 words including the column type.
        
        Example:
        "user" : 
        Please generate a detailed description of the following dataset.
        "assistent":  
        FoodItem Dataset
        This dataset contains information about food items, including their weight and caloric content per 100 grams.
        
        **Count of Values**:2,225 rows
                
        **Key columns**:

        **FoodItem**: Name of the food item.

        **per100grams**: Serving size, standardized to 100 grams for most items.

        **Cals_per100grams**: Number of calories contained in 100 grams of the respective food item.
   
        """,
        generation_config = genai.GenerationConfig(
            max_output_tokens=400,
            temperature=0,
        )
    )

        
    st.markdown(desc_response.text)
    
