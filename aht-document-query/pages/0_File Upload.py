import streamlit as st
import os
from databricks.sdk import WorkspaceClient
from functions import deploy_time
from pypdf import PdfReader
from pathlib import Path

# Ensure environment variable is set correctly
assert os.getenv('UPLOAD_VOLUME'), "UPLOAD_VOLUME must be set in app.yaml."
volume_uri = os.getenv("UPLOAD_VOLUME")
#import the workspace client for file uploads 
w = WorkspaceClient()

st.set_page_config(
    page_title="File Upload Tool",
    page_icon="📄",
)

st.sidebar.info("Last Deployment: {}".format(deploy_time()), icon="ℹ️")

st.title("📄 File Upload Tool")
st.subheader("Upload a file to Unity Catalog", divider="gray")
st.subheader("Use the text as context in an Chatbot using Llama 3.1")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    st.write(uploaded_file.name)

    type = Path(uploaded_file.name).suffix 
    if type == ".pdf":
        pdf = uploaded_file
        #read pdf and display text
        pdf_reader = PdfReader(pdf) # read your PDF file
        # extract the text data from your PDF file after looping through its pages
        text_data =""
        for page in pdf_reader.pages:
            text_data+= page.extract_text()
        st.write(text_data) # view the text data
        st.session_state.context = text_data

    if type == ".csv":
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

    #upload file to volumes
    try:
        file_name = uploaded_file.name
        file_contents = binary_data = uploaded_file.getvalue()
        w.files.upload(file_path=f'{volume_uri}/{file_name}', contents=file_contents, overwrite=True)
    except Exception as e:
        st.write(f'Error saving file: {str(e)}')

    


