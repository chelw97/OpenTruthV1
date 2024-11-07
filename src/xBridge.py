import os
import sys
import tweepy
sys.path.append(os.path.abspath('.'))

import lib.twAuto as twAuto
from src.logs import logs
from lib.scraper.twitter_scraper import Twitter_Scraper


from src.config import get_config,get_credentials
config=get_config()
credentials=get_credentials()

class xBridge:
    def __init__(self):
        self.client_selenium_action = twAuto.twAuto(
            username=credentials["TWITTER_user_name"],
            email=credentials["TWITTER_email"],
            password=credentials["TWITTER_pwd"],
            chromeDriverMode="auto", #if you use auto twAuto will automatically download the chrome driver for you,
                                                #if you use the manual option, you need to provide the driver path in driverPath parameter.
            # driverPath="your drivers path", #use only if you are using the chromeDriverMode in manual mode
            pathType="xPath", #It is testId by default. I highly recommend you to use testId instead of xPath. If you had any problems with library you can try the xPath mode too.
            headless=False, #Headless is true by default.
            debugMode= False, #Really poorly implemented debug mode, this is for reading occured errors.
                                    #It is not reliable right now but you can give it a try if you want to.
            createCookies= True #True by default.
        )
        self.client_official = tweepy.Client(
            bearer_token=credentials["TWITTER_API_BEARER_TOKEN"],
            access_token=credentials["TWITTER_API_ACCESS_TOKEN"],
            access_token_secret=credentials["TWITTER_API_ACCESS_TOKEN_SECRET"],
            consumer_key=credentials["TWITTER_API_CONSUMER_KEY"],
            consumer_secret=credentials["TWITTER_API_CONSUMER_SECRET"]
        )

        self.logs = logs()
        self.logs.log_info("xBridge initialized")
        self.client_selenium_read = None

    def init_client_selenium_read(self):
        self.client_selenium_read = Twitter_Scraper(
                        mail=None,
                        username=credentials['TWITTER_user_name'],
                        password=credentials['TWITTER_pwd'],
                        headless=config['headless']
                    )
        
    def get_tweet_core(self, username=None, hashtag=None, count=5):
        '''
        returns the tweets in csv(df) format with columns of:
        Name,Handle,Timestamp,Verified,Content,Comments,Retweets,Likes,Analytics,Tags,Mentions,Emojis,Profile Image,Tweet Link,Tweet ID
        '''
        def scrape():
            self.client_selenium_read.scrape_tweets(
                max_tweets=count,
                scrape_username=username,
                scrape_hashtag=hashtag,
            )
            
            # self.client_selenium_read.save_to_csv() #for debugging

            # if not self.client_selenium_read.interrupted:
            #     self.client_selenium_read.driver.close()
            return self.client_selenium_read.get_tweets_csv()
        
        if self.client_selenium_read is None or not self.client_selenium_read.login_bool:
            self.init_client_selenium_read()
            self.client_selenium_read.login()
            return scrape()
        else:
            try:
                return scrape()
            except Exception as e:
                self.logs.log_error("Error in get_tweet_core: "+str(e))
                self.init_client_selenium_read()
                self.client_selenium_read.login()
                return scrape()

            

    def get_home_timeline(self, count=5):
        return self.get_tweet_core(count=count)

    def get_tweet_via_username(self, username, count=5):
        return self.get_tweet_core(username=username, count=count)

    def get_tweet_via_hashtag(self, hashtag, count=5):
        return self.get_tweet_core(hashtag=hashtag, count=count)

    def reply(self, in_reply_to_tweet_id, text, image_path=""):
        self.tweet_core(text, in_reply_to_tweet_id=in_reply_to_tweet_id, image_path=image_path)
        self.logs.log_info("Replied to tweet with id: " + in_reply_to_tweet_id+" with text: "+text, "bold red", "Action")

    def quote(self, quote_tweet_id, text, image_path=""):
        self.tweet_core(text, quote_tweet_id=quote_tweet_id, image_path=image_path)
        self.logs.log_info("Quoted tweet with id: " + quote_tweet_id+" with text: "+text, "bold red", "Action")

    def like(self, url):
        self.client_selenium_action.start()
        self.client_selenium_action.login()
        self.client_selenium_action.like(url=url)
        self.client_selenium_action.close()
        self.logs.log_info("Liked tweet at url: " + url, "bold red", "Action")

    def tweet(self, text, in_reply_to_tweet_id=None, image_path="", quote_tweet_id=None):
        self.tweet_core(text, in_reply_to_tweet_id=in_reply_to_tweet_id, image_path=image_path, quote_tweet_id=quote_tweet_id)
        self.logs.log_info("Tweeted: " + text, "bold red", "Action")

    def tweet_core(self, text, in_reply_to_tweet_id=None, image_path="", quote_tweet_id=None):
        try:
            self.client_official.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_tweet_id, quote_tweet_id=quote_tweet_id)
        except Exception as e:
            self.logs.log_error("Fail to create tweet: "+str(e))

if __name__ == "__main__":
    xb = xBridge()
    # xb.tweet("Hello world!",1851122935165304847)
    print(xb.get_home_timeline())