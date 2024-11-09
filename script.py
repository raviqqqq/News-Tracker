import feedparser
import time
import pandas as pd
from newspaper import Article
from newspaper import Config
import lxml_html_clean

#Config information for newspaper library
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 180

#News Sources as per domains containing relevant RSS Feeds
headlines = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'toi':'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/trending/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_topstories.rss',
    'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
    'theguardian':'https://www.theguardian.com/international/rss'
}
tech = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/technology.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeeds/66949542.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/technology/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/sci-tech/science/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_technology.rss',
    'bbc':'http://feeds.bbci.co.uk/news/technology/rss.xml',
    'theguardian':'https://www.theguardian.com/uk/technology/rss'
}
business = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/business.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeedsvideo/3813458.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/business/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/business/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_news_international.rss',
    'bbc':'http://feeds.bbci.co.uk/news/business/rss.xml',
    'theguardian':'https://www.theguardian.com/uk/business/rss'
}
science = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/science/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/sci-tech/science/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_technology.rss',
    'bbc':'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'theguardian':'https://www.theguardian.com/science/rss'
}
sport = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeedsvideo/3813456.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/sports/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/sport/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_media.rss',
    'bbc':'https://news.bbc.co.uk/sport1/hi/help/rss/default.stm',
    'theguardian':'https://www.theguardian.com/uk/sport/rss'
}
entertainment = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeedsvideo/3812908.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/entertainment/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/entertainment/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_media.rss',
    'bbc':'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
    'theguardian':'https://www.theguardian.com/uk/culture/rss'
}
lifestyle = {
    'nytimes':'https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml',
    'toi':'http://timesofindia.indiatimes.com/rssfeedsvideo/3813443.cms',
    'htimes':'https://www.hindustantimes.com/feeds/rss/lifestyle/rssfeed.xml',
    'thehindu':'https://www.thehindu.com/life-and-style/feeder/default.rss',
    'cnn':'http://rss.cnn.com/rss/money_lifestyle.rss',
    'bbc':'http://feeds.bbci.co.uk/news/education/rss.xml',
    'theguardian':'https://www.theguardian.com/uk/lifeandstyle/rss'
}

#Function to return summary of news article
def get_summary(link):
    article = Article(link, config = config)
    
    #Summary may result in errors, hence try except block used 
    try:
        article.download()
        article.parse()
        article_meta_data = article.meta_data
        summary = {value for (key, value) in article_meta_data.items() if key == 'description'}
    except:
        return "Not Available"
    else:
        return list(summary)[0]

#Function to return news source based on domain
def get_domain(domain):
    if domain == "Headlines":
        return headlines
    elif domain == "Tech":
        return tech
    elif domain == "Business":
        return business
    elif domain == "Science":
        return science
    elif domain == "Sport":
        return sport
    elif domain == "Entertainment":
        return entertainment
    elif domain == "Lifestyle":
        return lifestyle

def get_source_site(site, news_sources):
    if site == "New York Times":
        news_sources = news_sources['nytimes']
    elif site == "Times of India":
        news_sources = news_sources['toi']
    elif site == "Hindustan Times":
        news_sources = news_sources['htimes']
    elif site == "The Hindu":
        news_sources = news_sources['thehindu']
    elif site == "CNN":
        news_sources = news_sources['cnn']
    elif site == "BBC":
        news_sources = news_sources['bbc']
    else:
        news_sources = news_sources['theguardian']
    return news_sources


#Main function
def news_search(keyword=None, domain = None, source_site = None):
    #Dataframe to store results
    df = pd.DataFrame({'Title':[], 'Published':[],'Link':[],'Summary':[]})

    #If source is selected
    if source_site!="All":
        #Obtaining news source based on the domain selected
        if domain == "Headlines":
            news_sources = get_domain("Headlines")
            news_sources = get_source_site(source_site, news_sources)
        elif domain == "Tech":
            news_sources = get_domain("Tech")
            news_sources = get_source_site(source_site, news_sources)
        elif domain == "Business":
            news_sources = get_domain("Business")
            news_sources = get_source_site(source_site, news_sources)
        elif domain == "Science":
            news_sources = get_domain("Science")
            news_sources = get_source_site(source_site, news_sources)
        elif domain == "Sport":
            news_sources = get_domain("Sport")
            news_sources = get_source_site(source_site, news_sources)
        elif domain == "Entertainment":
            news_sources = get_domain("Entertainment")
            news_sources = get_source_site(source_site, news_sources)
        else:
            news_sources = get_domain("Lifestyle")
            news_sources = get_source_site(source_site, news_sources)

            
        #Parse RSS Feed and obtain the articles
        news_feed = feedparser.parse(news_sources)
        entries = news_feed["entries"]

        #Code to execute based on the keyword specification
        #No keyword specified
        if keyword is None:
            for entry in entries:
                title = entry['title']
                published = entry['published']
                link = entry['link']
                summary = get_summary(link)
                temp = {'Title':title, 'Published':published,'Link':link,'Summary':summary}

                #Appending article information to the dataframe
                df = pd.concat([df, pd.DataFrame([temp])], ignore_index = True)
            return df
    
        #For each article, check if keyword is present in the title and subsequently obtain the relevant information
        else:
            for entry in entries:
                if keyword in str(entry["title"]):
                    title = entry['title']
                    published = entry['published']
                    link = entry['link']
                    summary = get_summary(link)
                    temp = {'Title':title, 'Published':published,'Link':link,'Summary':summary}

                    #Appending article information to the dataframe
                    df = pd.concat([df, pd.DataFrame([temp])], ignore_index = True)
            return df


    #Code to execute when ALL news sources is to be considered
    else:
        #Obtaining news source based on the domain selected
        if domain == "Headlines":
            news_sources = get_domain("Headlines")
        elif domain == "Tech":
            news_sources = get_domain("Tech")
        elif domain == "Business":
            news_sources = get_domain("Business")
        elif domain == "Science":
            news_sources = get_domain("Science")
        elif domain == "Sport":
            news_sources = get_domain("Sport")
        elif domain == "Entertainment":
            news_sources = get_domain("Entertainment")
        else:
            news_sources = get_domain("Lifestyle")
            
        #Code to execute based on the keyword specification
        #No keyword specified
        if keyword is None:
            for source in news_sources.values():
                #Parse RSS Feed and obtain the articles
                news_feed = feedparser.parse(source)
                entries = news_feed["entries"]

                #For each article, check if keyword is present in the title and subsequently obtain the relevant information
                for entry in entries:
                    title = entry['title']
                    published = entry['published']
                    link = entry['link']
                    summary = get_summary(link)
                    temp = {'Title':title, 'Published':published,'Link':link,'Summary':summary}

                    #Appending article information to the dataframe
                    df = pd.concat([df, pd.DataFrame([temp])], ignore_index = True)
            return df
        
        else:
            #Code to parse through each of the url and print the matched headlines
            for source in news_sources.values():
                #Parse RSS Feed and obtain the articles
                news_feed = feedparser.parse(source)
                entries = news_feed["entries"]

                #For each article, check if keyword is present in the title and subsequently obtain the relevant information
                for entry in entries:
                    if keyword in str(entry["title"]):
                        title = entry['title']
                        published = entry['published']
                        link = entry['link']
                        summary = get_summary(link)
                        temp = {'Title':title, 'Published':published,'Link':link,'Summary':summary}

                        #Appending article information to the dataframe
                        df = pd.concat([df, pd.DataFrame([temp])], ignore_index = True)
            return df
   