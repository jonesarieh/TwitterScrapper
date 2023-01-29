import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
import pymongo 
import streamlit as st


st.set_page_config(page_title = 'TwitterScrapper',layout ="wide")
st.title("Welcome to Twitter Scrapper")

tweets = []
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Date Range to be scrapped")
        st.text('Date should be YYYY-MM-DD (Example: 2023-01-31)')
        date1 = st.text_input('From Date:',key = 1)
 
        date2 = st.text_input('To Date:',key = 2)
        
        limit = st.text_input('Data Limit:',key =4)

    with right_column:
        st.subheader("Twitter Search")        
        user = st.text_input('Enter a Keyword to search:',key = 3)

        
    if len(user)>1:        
        with st.container():
            st.write("---")        
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{user} since:{date1} until:{date2}').get_items()):
                if i>int(limit): 
                    break
                tweets.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])
                
            df = pd.DataFrame(tweets, columns=['Date','Id','Url', 'Tweet_Content', 'User', 'Reply_Count', 'Retweet_Count','Language', 'Source', 'Like_Count'])
            # print(df) 
            dataframe = st.dataframe(df)
            if len(df)>1:
                 st.subheader("Upload the File in Database")
                 myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                 database = st.text_input('Create a database:',key = 5)
                 if len(database)>1:
                     mydb = myclient[database]
                 collection = st.text_input('Create a Collection:',key = 6)    
                 if len(collection)>1:
                     mycol = mydb[collection]
                     st.write("Succesfully Uploaded")
                     df.reset_index(inplace = True)
                     datadict = df.to_dict('records')
                    #st.write(datadict)
                     
                     csv = df.to_csv()
                     st.download_button(label="Download data as CSV file", data=csv, file_name='Twittercsv.csv',mime='text/csv',)
                 
                     mongo = mycol.insert_one({user:datadict})
