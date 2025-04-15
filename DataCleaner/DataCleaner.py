import streamlit as st
import pandas as pd
import os
from io import BytesIO
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;
        color: #333333;
    }
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        padding: 1rem;
        border-bottom: 2px solid #3498db;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #34495e;
        border-left: 4px solid #3498db;
        padding-left: 1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1.1rem;
        color: #7f8c8d;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Lottie Animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_excel = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")

# Title and Description
st.markdown("<h1 class='main-header'>💾💿📀💽 Data Sweeper</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<p class='info-text'>Transform your Excel files into CSV format with ease. Upload, clean, and convert your data in just a few clicks!</p>", unsafe_allow_html=True)
with col2:
    st_lottie(lottie_excel, height=150, key="excel_animation")

# File Uploader
st.markdown("<h2 class='sub-header'>📁 Upload Your Files</h2>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Choose Excel or CSV files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower().strip()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error("Invalid file format.")
            continue

        # File Details
        st.markdown(f"<h3 class='sub-header'>🔍 Data Preview: {file.name}</h3>", unsafe_allow_html=True)
        st.dataframe(df.head())

        # Data Cleaning Options
        st.markdown("<h3 class='sub-header'>🧼 Data Cleaning Options</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🔄 Remove Duplicates for {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")

            with col2:
                if st.button(f"🔢 Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled successfully!")

        st.markdown("<h3 class='sub-header'>🎯 Column Management</h3>", unsafe_allow_html=True)
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.markdown("<h3 class='sub-header'>📊 Visualization Tools</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Show data visualization for {file.name}"):
            numerical_data = df.select_dtypes(include=['number']).iloc[:, :2]
            
            numerical_data = numerical_data.apply(pd.to_numeric, errors='coerce')
            numerical_data = numerical_data.dropna()

            if not numerical_data.empty:
                st.bar_chart(numerical_data)
            else:
                st.info("No numerical data available for visualization.")

        # Conversion Options
        st.markdown("<h3 class='sub-header'>🔃 File Conversion</h3>", unsafe_allow_html=True)
        conversion_type = st.radio(f"Choose conversion type for {file.name}", ["CSV", "Excel"], key=file.name)
        if st.button(f"🚀 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False) 
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success(f"🎉 {file.name} converted successfully!")

else:
    st.info("👆 Upload your Excel or CSV files to get started!")

# # Imports
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# # Set up our App
# st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout="wide")
# st.title("💾💿📀💽 Data Sweeper")
# st.write("Transform Your files between CSV and Excel formats with built-in Data Cleaning and Visualization!")

# uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# # Flag to track if any files were processed
# files_processed = False  

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()

#         if file_ext == ".csv":
#             df = pd.read_csv(file)
#         elif file_ext == ".xlsx":
#             df = pd.read_excel(file, engine="openpyxl")
#         else:
#             st.error(f"Unsupported file type: {file_ext}")
#             continue

#         # Display info about the file
#         st.write(f"**📁 File Name:** {file.name}")
#         st.write(f"**🗄 File Size:** {file.size / 1024:.2f} KB")

#         # Show 5 rows of df
#         st.write("🔍 Preview the Head of the DataFrame")
#         st.dataframe(df.head())

#         # Options for data cleaning
#         st.subheader("🧼 Data Cleaning Options")
#         if st.checkbox(f"Clean Data For {file.name}"):
#             col1, col2 = st.columns(2)

#             with col1:
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("✅ Duplicates Removed!")

#             with col2:
#                 if st.button(f"Fill Missing Values for {file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("✅ Missing Values have been Filled!")

#         # Choose Specific Columns to Keep or Convert
#         st.subheader("🎯 Select Columns to Convert")
#         columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
#         df = df[columns]

#         # Data Visualization
#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

#         # Convert the File -> CSV to Excel
#         st.subheader("🔃 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

#         # Initialize buffer
#         buffer = BytesIO()

#         if st.button(f"Convert {file.name}"):
#             if conversion_type == "CSV":
#                 df.to_csv(buffer, index=False)
#                 file_name = file.name.replace(file_ext, ".csv")
#                 mime_type = "text/csv"

#             elif conversion_type == "Excel":
#                 with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
#                     df.to_excel(writer, index=False)
#                 file_name = file.name.replace(file_ext, ".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

#             buffer.seek(0)

#             # Download Button
#             st.download_button(
#                 label=f"👇 Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

#             # Set flag to True since at least one file has been processed
#             files_processed = True  

# # Show success message only if at least one file was processed
# if files_processed:
#     st.success("🥳 All files processed!")  
      



