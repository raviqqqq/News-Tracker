# News Tracker
This project is aimed at data collection. It allows the user to obtain news articles by the keyword, specific source, specific news domain, or even a combination of the three.
The articles are obtained from multiple sources such as NY Times, Times of India, BBC, CNN and others. 

The project was created using:
1. Streamlit - To create the web app, allowing the creation of user input widgets.
2. Feedparser and Newspaper - To parse through the news sources and obtain the details of the required articles, such as the title, source, summary and others. 
3. Pandas - To create the resultant dataframe, containing details of the all the news articles retrieved.

Note: The dependencies are listed in the requirements.txt file. Issues may arise when the app is deployed with varying dependencies.

You can access the application via:
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://the-news-tracker.streamlit.app)
