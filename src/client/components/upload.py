import streamlit as st
from utils.api import upload_url_api


def render_uploader():

    # Display a heading in the sidebar for the url upload section.
    st.sidebar.header("Upload URL of the YT Video")

    # Display an uploader.
    uploaded_url = st.sidebar.text_input(
        "Enter YouTube Video URL"
    )

    # Upload the selected URL only when:
    # The user clicks the "Upload URL" button.

    if st.sidebar.button("Upload URL") and uploaded_url:

        # Send the uploaded URL to the FastAPI backend,
        # where it will be processed, embedded, and stored
        # in the Pinecone vector database.
        response = upload_url_api(uploaded_url)

        # Check whether the backend successfully processed
        # the uploaded document.
        if response.status_code == 200:

            # Display a success message in the sidebar.
            st.sidebar.success("Uploaded successfully")

        else:

            # Display the error message returned by the backend.
            st.sidebar.error(f"Error:{response.text}")