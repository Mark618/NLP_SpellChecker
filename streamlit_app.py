import streamlit as st
import pickle
import pandas as pd
import numpy as np
import nltk
import spacy
import os

import logging

# python -m spacy download en_core_web_sm

CURRENT_DIR = os.getcwd()

@st.cache_resource
def spacy_tokenize():
    
    nlp = spacy.load("en_core_web_sm",exclude=["tok2vec","parser", "ner"])
    
    return nlp

@st.cache_resource
def detect_model():
    with open(os.path.join(CURRENT_DIR,"model/model.pkl"),"rb") as p:
        model = pickle.load(p)
        
    return model


def main():
    st.title("Medical Spell Checker")
    st.markdown("""
                #### Description
                Check for spelling errors in medical and healthcare-related terms. 
                """)
    st.markdown('___')
    st.sidebar.subheader("About the App")
    st.sidebar.write("A probabilistic model for detecting of spelling errors and correct spelling errors")
    st.sidebar.info("Given a misspelled word, find the most likely correction(s) from a medical dictionary.")
    st.sidebar.subheader("Developed by")
    st.sidebar.write("Mick Yean Tuck Fei tp044713@mail.apu.edu.my")
    st.sidebar.write("Mark Yean Tuck Ming tp044716@mail.apu.edu.my")
    
    c = st.container()
    text = c.text_area("Paste Medical Text","Paste text to get spelling suggestions for though terms such as glcoauma",max_chars=500,label_visibility="hidden")

if __name__ == '__main__':
    main()
