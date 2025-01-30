import pandas as pd 
import streamlit as st 
import google.generativeai as genai
from secret import gemini_key
from helpers import basic_analysis

def data_description(df):
    analysis = basic_analysis(df)
    data_description_prompt =  f"""Please generate a detailed description of the following dataset:
        This is a basic analysis and sample data :{analysis}
        The description should include:
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
    return data_description_prompt
        
    
