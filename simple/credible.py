import openai
import streamlit as st

openai.api_key = st.secrets['pass']

st.header("Credibility of a Tweet Based on it's Content.")

article_text = st.text_area("Enter the content of a tweet")

if st.button("Determine Credibility"):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = "please determine if the content of this is true or false :" + article_text,
        max_tokens = 6,
        temperature = 0.9
    )

    res = response["choices"][0]["text"]
    st.info(res)
    #st.download_button("download result", res)
else:
    st.warning("enter the content of a tweet")