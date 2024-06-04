import pickle
import streamlit as st
import numpy as np
import requests
from io import BytesIO

# Function to download file from Google Drive
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

# Helper functions for file download
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Download the models from Google Drive
download_file_from_google_drive('16m5p44GAexPMRtJ3GwH1L_CWz4G4JMve', 'diabetic_model.sav')
download_file_from_google_drive('ANOTHER_ID', 'parkinsson_disease.sav')  # Replace 'ANOTHER_ID' with the corresponding file ID

# Load the models
parkinsson_model = pickle.load(open('parkinsson_disease.sav', 'rb'))

# Sidebar for navigation
with st.sidebar:
    st.title('Disease Prediction System')
    selected = st.radio('Select Disease', ['Parkinsson Disease Prediction'])

# Parkinsson Disease Prediction
if selected == 'Parkinsson Disease Prediction':
    st.title('Parkinsson Prediction using ML')
    MDVPFo = st.text_input('MDVP:Fo(Hz)')
    MDVPFhi = st.text_input('MDVP:Fhi(Hz)')
    MDVPFlo = st.text_input('MDVP:Flo(Hz)')
    MDVPJitter = st.text_input('MDVP:Jitter(%)')
    MDVPJitterAbs = st.text_input('MDVP:Jitter(Abs)')
    MDVPRAP = st.text_input('MDVP:RAP')
    MDVPPPQ = st.text_input('MDVP:PPQ')
    JitterDDP = st.text_input('Jitter:DDP')
    MDVPShimmer = st.text_input('MDVP:Shimmer')
    MDVPShimmer_dB = st.text_input('MDVP:Shimmer(dB)')
    ShimmerAPQ3 = st.text_input('Shimmer:APQ3')
    ShimmerAPQ5 = st.text_input('Shimmer:APQ5')
    MDVPAPQ = st.text_input('MDVP:APQ')
    ShimmerDDA = st.text_input('Shimmer:DDA')
    NHR = st.text_input('NHR')
    HNR = st.text_input('HNR')
    RPDE = st.text_input('RPDE')
    DFA = st.text_input('DFA')
    spread1 = st.text_input('spread1')
    spread2 = st.text_input('spread2')
    D2 = st.text_input('D2')
    PPE = st.text_input('PPE')

    result = ""
    if st.button('Check for Parkinson'):
        prediction2 = parkinsson_model.predict([[MDVPFo, MDVPFhi, MDVPFlo, MDVPJitter, MDVPJitterAbs, MDVPRAP, MDVPPPQ, JitterDDP, MDVPShimmer, MDVPShimmer_dB, ShimmerAPQ3, ShimmerAPQ5, MDVPAPQ, ShimmerDDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])
        if prediction2[0] == 0:
            result = 'The person does not have Parkinson\'s disease.'
        else:
            result = 'The person has Parkinson\'s disease.'
    st.success(result)
