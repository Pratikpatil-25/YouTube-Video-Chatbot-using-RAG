import requests
from config import API_URL

import requests
from config import API_URL


def upload_url_api(video_url):
    """
    Sends the YouTube video URL to the backend.

    The backend endpoint should receive it as:
        video_url: str = Form(...)

    The data is sent as 'application/x-www-form-urlencoded'
    because we're using the 'data' parameter.
    """

    return requests.post(
        f"{API_URL}/upload_url/",
        data={"url": video_url}
    )



def ask_question(question):
    # Sends the user's question as form data to the backend.
    # The backend receives it as:
    # question: str = Form(...)
    return requests.post(
        f"{API_URL}/ask/",
        data={"question": question}
    )