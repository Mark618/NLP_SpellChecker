import streamlit as st
import pickle
import pandas as pd
import numpy as np
import nltk
import spacy
import os

import logging
import additional_func

# python -m spacy download en_core_web_sm

CURRENT_DIR = os.getcwd()

@st.cache_resource
def spacy_tokenize():    
    nlp = spacy.load("en_core_web_sm",exclude=["tok2vec","parser", "ner"])    
    return nlp

@st.cache_resource
def detect_model():
    # Load NLTK language model
    with open(os.path.join(CURRENT_DIR,"model/model.pkl"),"rb") as p:
        model = pickle.load(p)        
    return model

@st.cache_resource
def word_dict():
    # Get unique words
    with open(os.path.join(CURRENT_DIR,"data/processed_texts.pkl"),"rb") as p:
        word_list = pickle.load(p)    
        
    word_dict = {}
    for row in word_list:
        for word in row:
            if word not in word_dict:
                word_dict[word] = len(word)                
    return word_dict    

nlp = spacy_tokenize()
model = detect_model()
wl_process = word_dict()
spell_crrct_obj = additional_func.SpellCorrection(nlp,model) 


def main():
    st.title("Medical Spell Checker")
    st.markdown("""
                #### Description
                Check for spelling errors in medical and healthcare-related terms.Dictionary is restricted to biomedical terminology. Check is not case-sensitive. 
                """)
    st.markdown('___')
    
     # Sidebar section
    st.sidebar.subheader("About the App")
    st.sidebar.write("A probabilistic model for detecting of spelling errors and correct spelling errors")
    st.sidebar.info("Given a misspelled word, find the most likely correction(s) from a medical dictionary.")
    st.sidebar.subheader("Developed by")
    st.sidebar.write("Mick Yean Tuck Fei tp044713@mail.apu.edu.my")
    st.sidebar.write("Mark Yean Tuck Ming tp044716@mail.apu.edu.my")
    
    
    
    if "input_text" not in st.session_state:
        st.session_state.input_text = "Paste text to get spelling suggestions for though terms such as glauasdcoma,liveer,herat" 
        
    st.session_state.input_text = st.text_area("Paste Medical Text", st.session_state.input_text,max_chars=500,label_visibility="hidden", key="text_area")  
         
    if "clicked" not in st.session_state:
        st.session_state.clicked = False
    
    if st.button("Check") or st.session_state["clicked"]:
        st.session_state["clicked"] = True
        wrong_words,words_pos,temp_sent = spell_crrct_obj.detect_spell_error(st.session_state.input_text)
        if len(words_pos) ==0:
            st.write("No spelling error detected/ No match found.")
        else:
            st.write("Result")
            for i,word in enumerate(wrong_words):
                sorted_keys = spell_crrct_obj.possible_words(wl_process,word)
                st.write(f"Found possible wrong words: {word[1]}")
                
                # option = st.selectbox(
                #             "Suggestion",
                #             sorted_keys,
                #             index=None,
                #             placeholder="Select words...",
                #         )
                # st.write("You selected:", option)
                
                for s in sorted_keys:
                    key_val = f"button_{s}"                    
                    if st.button(label=s,key=key_val):
                        temp_sent[words_pos[i]]=s
                        new_sent = " ".join(temp_sent)
                        st.session_state.input_text = new_sent                        
                        st.session_state["clicked"] = True
                        

    

if __name__ == '__main__':
    main()
