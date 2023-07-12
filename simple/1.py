import tweepy
import streamlit as st
import openai
import pandas as pd

# Twitter API credentials
consumer_key = st.secrets['consumerkey']
consumer_secret = st.secrets['consumersecret']
access_token = st.secrets['accesstoken']
access_token_secret = st.secrets['accesstokensecret']

# OpenAI API credentials
openai_api_key = st.secrets['pass']
openai.api_key = openai_api_key

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Streamlit app
st.title("Twitter Credibility Checker")

# Input Twitter username
username = st.text_input("Enter Twitter username (seprated by commas)")
counter = st.text_input("Enter the number of tweets")
start_date = st.date_input("Start date")
end_date = st.date_input("End date")
# Fetch and display live tweets
if st.button("Fetch Tweets"):
    try:
        username_list = [username.strip() for username in username.split(",")]
        data = []
        for username in username_list:
            tweets = api.user_timeline(screen_name=username, count=counter)
            #st.write(f"Latest tweets from {username}:")
            for tweet in tweets:
            #st.write(tweet.text)
            #st.write("Credibility Score:")
             if start_date <= tweet.created_at.date() <=end_date:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt="please only determine if the content of this is true or false :" + tweet.text,
                    max_tokens=5,
                    temperature=0.3,
                    n=1,
                    stop=".",
                )
                credibility_score = response.choices[0].text.strip()
                data.append({"Username":username, "Tweet": tweet.text, "Credibility Score": credibility_score, "Posted Date": tweet.created_at.date()})
        
        df=pd.DataFrame(data)
        st.write("Latest tweets and their credibility scores:")
        st.dataframe(df)

        #st.write(credibility_score)
    except tweepy.TweepyException as e:
        st.error(f"Error fetching tweets: {str(e)}")