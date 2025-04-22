# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout="wide")
st.title("💾💿📀💽 Data Sweeper")
st.write("Transform Your files between CSV and Excel formats with built-in Data Cleaning and Visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Flag to track if any files were processed
files_processed = False

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            try:
                df = pd.read_csv(file)
                # Remove all columns with "Unnamed" in their name
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            except Exception as e:
                st.error(f"Error reading CSV file '{file.name}': {e}")
                continue
        elif file_ext == ".xlsx":
            try:
                df = pd.read_excel(file, engine="openpyxl")
                # Remove all columns with "Unnamed" in their name
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            except Exception as e:
                st.error(f"Error reading Excel file '{file.name}': {e}")
                continue
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**📁 File Name:** {file.name}")
        st.write(f"**🗄 File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of df
        st.write("🔍 Preview the Head of the DataFrame")
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

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_cols_viz = df.select_dtypes(include=['number']).columns
            if not numeric_cols_viz.empty:
                try:
                    if len(numeric_cols_viz) >= 2:
                        st.bar_chart(df[numeric_cols_viz[:2]])
                    elif len(numeric_cols_viz) == 1:
                        st.bar_chart(df[numeric_cols_viz])
                    else:
                        st.warning("No suitable numeric columns for bar chart visualization.")
                except Exception as e:
                    st.error(f"Error during visualization for '{file.name}': {e}")
            else:
                st.info("No numeric columns available for visualization.")

        # Convert the File -> CSV to Excel
        st.subheader("🔃 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Initialize buffer
        buffer = BytesIO()

        if st.button(f"Convert {file.name}"):
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
                mime=mime_type
            )

            # Set flag to True since at least one file has been processed
            files_processed = True

# Show success message only if at least one file was processed
if files_processed:
    st.success("🥳 All files processed!")
