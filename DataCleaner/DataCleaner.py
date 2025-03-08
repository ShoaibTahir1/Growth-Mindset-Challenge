# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout="wide")
st.title("💾💿📀💽 Data Sweeper")
st.write("Transform Your files between CSV and Excel formats with built-in Data Cleaning and Visualization!")

# Initialize session state for tracking downloads
if "files_processed" not in st.session_state:
    st.session_state["files_processed"] = False

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # 🔹 Fix Arrow Conversion Issues: Convert all object-type columns to string
        df = df.astype({col: "string" for col in df.select_dtypes(include=["object"]).columns})

        # Display info about the file
        st.write(f"**📁 File Name:** {file.name}")
        st.write(f"**🗄 File Size:** {file.getbuffer().nbytes / 1024:.2f} KB")

        # Show 5 rows of df
        st.write("🔍 Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("🧼 Data Cleaning Options")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values have been Filled!")

        # Choose Specific Columns to Keep or Convert  
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the File -> CSV to Excel
        st.subheader("🔃 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"👇 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
                on_click=lambda: st.session_state.update({"files_processed": True})  # Update session state
            )

# Show success message only if at least one file has been downloaded
if st.session_state["files_processed"]:
    st.success("🥳 All files processed!")  

  
    
          
            
        
            



