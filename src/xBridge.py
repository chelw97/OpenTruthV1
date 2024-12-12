import os
import sys
import tweepy
import tweepy.errors
sys.path.append(os.path.abspath('.'))

from src.config import get_config,get_credentials
from src.logs import logs
config=get_config()
credentials=get_credentials()


class xBridge:
    def __init__(self,scrape):
        self.scrape=scrape
        self.logs = logs()
        if scrape:
            import lib.twAuto as twAuto
            from lib.scraper.twitter_scraper import Twitter_Scraper
            self.client_selenium_action = twAuto.twAuto(
                username=credentials["TWITTER_user_name"],
                email=credentials["TWITTER_email"],
                password=credentials["TWITTER_pwd"],
                chromeDriverMode="auto", #if you use auto twAuto will automatically download the chrome driver for you,
                                                    #if you use the manual option, you need to provide the driver path in driverPath parameter.
                # driverPath="your drivers path", #use only if you are using the chromeDriverMode in manual mode
                pathType="testId", #It is testId by default. I highly recommend you to use testId instead of xPath. If you had any problems with library you can try the xPath mode too.
                headless=False, #Headless is true by default.
                debugMode= True, #Really poorly implemented debug mode, this is for reading occured errors.
                                        #It is not reliable right now but you can give it a try if you want to.
                createCookies= True #True by default.
            )
            self.logs.log_info("xBridge starting")
            self.client_selenium_action.start()
            self.client_selenium_action.login()
            self.client_selenium = Twitter_Scraper(
                        mail=None,
                        username=credentials['TWITTER_user_name'],
                        password=credentials['TWITTER_pwd']
                    )
        else:
            self.client_selenium = None

        self.client_official = tweepy.Client(
                bearer_token=credentials["TWITTER_API_BEARER_TOKEN"],
                access_token=credentials["TWITTER_API_ACCESS_TOKEN"],
                access_token_secret=credentials["TWITTER_API_ACCESS_TOKEN_SECRET"],
                consumer_key=credentials["TWITTER_API_CONSUMER_KEY"],
                consumer_secret=credentials["TWITTER_API_CONSUMER_SECRET"]
            )

        self.logs.log_info("xBridge initialized")

    def get_tweet_core(self, username=None, hashtag=None, count=5):
        '''
        returns the tweets in csv(df) format with columns of:
        Name,Handle,Timestamp,Verified,Content,Comments,Retweets,Likes,Analytics,Tags,Mentions,Emojis,Profile Image,Tweet Link,Tweet ID
        '''
        def scrape():
            self.client_selenium.scrape_tweets(
                max_tweets=count,
                scrape_username=username,
                scrape_hashtag=hashtag,
            )
            
            # self.client_selenium.save_to_csv() #for debugging

            # if not self.client_selenium.interrupted:
            #     self.client_selenium.driver.close()
            return self.client_selenium.get_tweets_csv()
        if not self.client_selenium.login_bool:
            self.client_selenium.login()
            return scrape()
        else:
            try:
                return scrape()
            except Exception as e:
                self.logs.log_error("Error in get_tweet_core: "+str(e))
                self.client_selenium.login()
                return scrape()

    def tweet_selenium(self, text,in_reply_to_tweet_id, quote_tweet_id,img_path=None):
        if in_reply_to_tweet_id:
            self.client_selenium_action.reply(text=text, tweet_id=in_reply_to_tweet_id, imgpath=img_path)
        elif quote_tweet_id:
            self.logs.log_info("Quoting is not implemented in twAuto, using reply instead")
            self.client_selenium_action.reply(text=text, tweet_id=quote_tweet_id, imgpath=img_path)
        else:
            self.client_selenium_action.tweet(text=text, imgpath=img_path)
        self.logs.log_info("Tweeted via selenium")

    def get_home_timeline(self, count=5):
        return self.get_tweet_core(count=count)

    def get_tweet_via_username(self, username, count=5):
        return self.get_tweet_core(username=username, count=count)

    def get_tweet_via_hashtag(self, hashtag, count=5):
        return self.get_tweet_core(hashtag=hashtag, count=count)

    def reply(self, in_reply_to_tweet_id, text, image_path=""):
        self.tweet_core(text, in_reply_to_tweet_id=in_reply_to_tweet_id, image_path=image_path)
        self.logs.log_info("Replied to tweet with id: " + in_reply_to_tweet_id+" with text: "+text)

    def quote(self, quote_tweet_id, text, image_path=""):
        self.tweet_core(text, quote_tweet_id=quote_tweet_id, image_path=image_path)
        self.logs.log_info("Quoted tweet with id: " + quote_tweet_id+" with text: "+text)

    def like(self, url):
        self.client_selenium_action.start()
        self.client_selenium_action.login()
        self.client_selenium_action.like(url=url)
        self.client_selenium_action.close()
        self.logs.log_info("Liked tweet at url: " + url)

    def tweet(self, text, in_reply_to_tweet_id=None, image_path="", quote_tweet_id=None):
        self.tweet_core(text, in_reply_to_tweet_id=in_reply_to_tweet_id, image_path=image_path, quote_tweet_id=quote_tweet_id)
        self.logs.log_info("Tweeted:\n" + text)

    def tweet_core(self, text, in_reply_to_tweet_id=None, image_path=None, quote_tweet_id=None):
        if self.scrape:
            self.tweet_selenium(text,in_reply_to_tweet_id=in_reply_to_tweet_id, quote_tweet_id=quote_tweet_id,img_path=image_path)
        else:
            try:
                self.client_official.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_tweet_id, quote_tweet_id=quote_tweet_id)
            except tweepy.errors.TooManyRequests as e:
                self.logs.log_error("429 too many requests: "+str(e))
            except Exception as e:
                self.logs.log_error("Fail to create tweet: "+str(e),exc_info=True)


if __name__ == "__main__":
    xb = xBridge(scrape=False)
    xb.tweet("Hello world!",1851122935165304847)
    # print(xb.get_home_timeline())