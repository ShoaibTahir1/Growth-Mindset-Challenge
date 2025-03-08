# #Imports

# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# #Set up our App and for emojis use "windows key" + "."

# st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout= "wide")
# st.title("💾💿📀💽 Data Sweeper")
# st.write("Transform Your files between CSV and Excel formats with built-in Data Cleaning and Visualization!")

# uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()


#         if file_ext == ".csv":
#             df = pd.read_csv(file)
#         elif file_ext == ".xlsx":
#             df= pd.read_excel(file)
#         else:
#             st.error(f"Unsupported file type: {file_ext}")
#             continue
        
# # Display info about the file
        
#         st.write(f"**📁 File Name:** {file.name}")
#         st.write(f"**🗄 File Size:** {file.size/1024}")
        
# # Show 5 rows of df
       
#         st.write("🔍 Preview the Head of the Dataframe")
#         st.dataframe(df.head())
        
# # Options for data cleaning
       
#         st.subheader("🧼 Data Cleaning Options")
#         if st.checkbox(f"Clean Data For {file.name}"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("Duplicates Removed!")
            
#             with col2:
#                 if st.button(f"Fill Missing Values for {file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("Missing Values have been Filled!")

# # Choose Specific Columns to Keep or Convert  
                    
#         st.subheader("🎯Select Columns to Convert")
#         columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
#         df = df[columns]
        
# # Create Some Visualizations

#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            
# # Convert the File -> CSV to Excel

#         st.subheader("🔃 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
#         if st.button (f"Convert {file.name}"):
#             buffer = BytesIO()
#             if conversion_type == "CSV":
#                 df.to_csv(buffer,index=False)
#                 file_name = file.name.replace(file_ext,".csv")
#                 mime_type = "text/csv"
             
#             elif conversion_type == "Excel":
#                 df.to_excel(buffer,index=False)
#                 file_name = file.name.replace(file_ext,".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
#             buffer.seek(0)
            
# # Download Button

#         st.download_button(
#             label = f"👇 Download {file.name} as {conversion_type}",
#             data = buffer,
#             file_name = file_name,
#             mime = mime_type)    
 
# st.success("🥳 All files processed!")            

# # Imports
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO
# import openpyxl

# # Set up the App
# st.set_page_config(page_title="💾💿📀💽 Data Sweeper", layout="wide")
# st.title("💾💿📀💽 Data Sweeper")
# st.write("Transform your files between CSV and Excel formats with built-in Data Cleaning and Visualization!")

# # Initialize session state for tracking downloads
# if "files_processed" not in st.session_state:
#     st.session_state["files_processed"] = False

# uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()

#         # Read file based on extension
#         if file_ext == ".csv":
#             df = pd.read_csv(file)
#         elif file_ext == ".xlsx":
#             df = pd.read_excel(file, engine="openpyxl")  # Ensure Excel files are read properly
#         else:
#             st.error(f"Unsupported file type: {file_ext}")
#             continue

#         # Store the original DataFrame in session state to keep track of changes
#         if f"df_{file.name}" not in st.session_state:
#             st.session_state[f"df_{file.name}"] = df.copy()

#         # Convert object-type columns to strings to fix Arrow conversion issues
#         st.session_state[f"df_{file.name}"] = st.session_state[f"df_{file.name}"].astype(
#             {col: "string" for col in st.session_state[f"df_{file.name}"].select_dtypes(include=["object"]).columns}
#         )

#         # Display file info
#         file_size_kb = file.getbuffer().nbytes / 1024
#         file_size_display = f"{file_size_kb:.2f} KB" if file_size_kb < 1024 else f"{file_size_kb / 1024:.2f} MB"
        
#         st.write(f"**📁 File Name:** {file.name}")
#         st.write(f"**🗄 File Size:** {file_size_display}")

#         # Show preview of the DataFrame
#         st.write("🔍 Preview the Head of the Dataframe")
#         st.dataframe(st.session_state[f"df_{file.name}"].head())

#         # Data Cleaning Options
#         st.subheader("🧼 Data Cleaning Options")
#         if st.checkbox(f"Clean Data for {file.name}"):

#             col1, col2 = st.columns(2)

#             with col1:
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     st.session_state[f"df_{file.name}"].drop_duplicates(inplace=True)
#                     st.write("✅ Duplicates Removed!")

#             with col2:
#                 if st.button(f"Fill Missing Values for {file.name}"):
#                     numeric_cols = st.session_state[f"df_{file.name}"].select_dtypes(include=['number']).columns
#                     st.session_state[f"df_{file.name}"][numeric_cols] = st.session_state[f"df_{file.name}"][numeric_cols].fillna(
#                         st.session_state[f"df_{file.name}"][numeric_cols].mean()
#                     )
#                     st.write("✅ Missing Values have been Filled!")

#         # Column Selection
#         st.subheader("🎯 Select Columns to Keep")
#         columns = st.multiselect(f"Choose Columns for {file.name}", st.session_state[f"df_{file.name}"].columns, default=st.session_state[f"df_{file.name}"].columns)
#         st.session_state[f"df_{file.name}"] = st.session_state[f"df_{file.name}"][columns].copy()

#         # Data Visualization
#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {file.name}"):
#             numeric_data = st.session_state[f"df_{file.name}"].select_dtypes(include=['number'])
#             if not numeric_data.empty:
#                 st.bar_chart(numeric_data.iloc[:, :2])  # Show first two numeric columns
#             else:
#                 st.write("⚠ No numeric data available for visualization!")

#         # File Conversion
#         st.subheader("🔃 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

#         if st.button(f"Convert {file.name}"):
#             buffer = BytesIO()
#             if conversion_type == "CSV":
#                 st.session_state[f"df_{file.name}"].to_csv(buffer, index=False)
#                 file_name = file.name.replace(file_ext, ".csv")
#                 mime_type = "text/csv"
#             elif conversion_type == "Excel":
#                 with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
#                     st.session_state[f"df_{file.name}"].to_excel(writer, index=False)
#                 file_name = file.name.replace(file_ext, ".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

#             buffer.seek(0)  # Reset buffer before download

#             # Download Button
#             st.download_button(
#                 label=f"👇 Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type,
#                 on_click=lambda: st.session_state.update({"files_processed": True})  # Update session state
#             )

# # Show success message if at least one file has been processed
# if st.session_state["files_processed"]:
#     st.success("🥳 All files processed successfully!")

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
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
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
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

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
      



