import streamlit as st 
import pandas as pd 
import google.generativeai as genai
from secret import gemini_key 
from helpers import basic_analysis, columns_description

def data_cleaning(df):
        analysis = basic_analysis(df)
        columns_desc = columns_description(df)
        data_cleaning_prompt =  f""" 
                This is a basic analysis and sample data : {analysis}. 
                Columns description: {columns_desc} 
                Please analyze the dataset and perform the following checks:
                - Check for Duplicates
                - Check Data Types
                - Check for Outliers
                - Check for Inconsistent Formatting
                - Check for Validity of Data
                - Check for Duplicate or Redundant Features
                - Check for Uniformity in Categorical Variables
                - Check for Data Consistency Across Columns
                - Check for Unnecessary Columns
                - Check for Date and Time Consistency
                - Check for Range Violations
                - Check for Categorical Imbalances
                - Check for Logical Inconsistencies Between Columns
                - Check for Standardization Across Units
                - Check for Missing Categorical Values
                - Check for Leading/Trailing Whitespace
                - Check for Data Entry Errors (Typos)
                - Check for Date/Time Gaps
                - Check for Aggregation Consistency
                - Check for Deprecated or Obsolete Data
                - Check for Temporal Consistency
                - Check for Data Shifts or Changes Over Time
                - Check for Inconsistent Encoding
                - Check for Consistent Data Grouping
                - Check for Proper Normalization or Scaling
                - Check for Correct Labeling and Target Variable Integrity
                - Check for Duplicated Identifiers Across Multiple Tables
                - Check for Consistency in Data Sources
                - Check for Data Granularity Consistency
                Please provide any findings and recommendations based on the dataset summary, highlighting potential issues and suggestions for fixes.
                if there is no issues wirte : Your data is clean! 
                if there is some issues only mention the issues in points.
                I NEED YOU TO MENTION THE PROBLEM AND LIST THE COLUMNS EFFECTED.
                
                
                Example answer:
                Issues Identified in Your Dataset:
                1. Missing Values:
                Brand: 20 records with missing values.
                Price: 40 records with missing values.
                2. Inconsistent Formats:
                Product Name: 80 records with inconsistent format.
                Date: 100 records with inconsistent format.
                3. Wrong Data Types:
                Price: Incorrect data type.
                Name: Incorrect data type.
                Suggestions for Addressing the Issues:
                1. Handling Missing Values:
                For the "Brand" column:

                - Fill missing values with the most frequent brand (Radio option).
                - Delete the rows with missing values (Radio option).
                For the "Price" column:
                -Fill missing values with the median price (Radio option).
                -Fill missing values with the mean price (Radio option).
                - Fill missing values with the mid value (Radio option).
                - Delete the rows with missing values (Radio option).


                """
        return data_cleaning_prompt