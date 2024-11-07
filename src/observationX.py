import os
import sys
sys.path.append(os.path.abspath('.'))

from dotenv import load_dotenv
from src.config import get_config,get_credentials
config=get_config()
credentials=get_credentials()

from interface.observationInterface import observationInterface
from src.xBridge import xBridge

class observationX(observationInterface):
    def __init__(self):
        load_dotenv()
        self.config=config
        self.xBridge_instance = xBridge()

    def get(self):
        return self.get_home_timeline()
        # return self.get_test()

    def get_test(self):
        import pandas as pd

        return pd.read_csv('tweets/observation_test.csv')

    def get_home_timeline(self, count=5):
        return self.xBridge_instance.get_home_timeline(count)
        
    def get_tweet_via_username(self,username,count=5):
        return self.xBridge_instance.get_tweet_via_username(username,count)

    def get_tweet_via_hashtag(self,hashtag,count=5):
        return self.xBridge_instance.get_tweet_via_hashtag(hashtag,count)
        

if __name__ == '__main__':
    ob = observationX()
    print(ob.get_home_timeline())
    # print(ob.get_tweet_via_username('elonmusk'))
    # print(ob.get_tweet_via_hashtag('AI'))