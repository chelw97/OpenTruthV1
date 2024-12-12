import os
import sys
sys.path.append(os.path.abspath('.'))


from interface.actionInterface import actionInterface
from src.xBridge import xBridge
from src.logs import logs


class actionX(actionInterface):
    def __init__(self,xBridge_instance: xBridge) -> None:
        self.logs = logs()
        self.logs.log_info("actionX initialized")
        self.xBridge_instance = xBridge_instance
        
    def excute(self, action:dict):
        '''
        Executes the action
        action example: 
        {
            "target_tweet_id": "target_tweet_id here",
            "action": "reply",
            "content": "content here"
        }
        '''
        target_tweet_id=action['target_tweet_id']
        action_decided=action['action']
        content=action['content']
        image_path="imgs/logo.jpg"
        if action_decided == 'tweet':
            self.tweet(message=content)
        elif action_decided == 'reply':
            self.reply(tweet_id=target_tweet_id, message=content,image_path=image_path)
        elif action_decided == 'quote':
            self.quote(tweet_id=target_tweet_id, message=content)
        else:
            if action['target_tweet_id']:
                self.reply(tweet_id=target_tweet_id, message=content,image_path=image_path)
            self.logs.log_error('Invalid action: '+action_decided)
            pass


    def reply(self, tweet_id, message, image_path=None):
        '''
        Replies to a tweet with a message
        '''
        self.xBridge_instance.reply(tweet_id, message, image_path)

    def quote(self, tweet_id, message, image_path=None):
        '''
        Quotes a tweet
        '''
        self.xBridge_instance.quote(tweet_id,message, image_path)

    def tweet(self, message, image_path=None):
        '''
        Posts a tweet
        '''
        self.xBridge_instance.tweet(message, image_path=image_path)


if __name__ == '__main__':
    action = actionX()
    # action.tweet('Hello World!'+str(datetime.datetime.now()))
    # action.reply("1851196765975760915", 'Hello World!'+str(datetime.datetime.now()))
    # action.quote("1851196765975760915", 'Hello World!'+str(datetime.datetime.now()))