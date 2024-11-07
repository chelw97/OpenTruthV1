import os
import sys
sys.path.append(os.path.abspath('.'))

import pandas as pd
import json
from src.config import get_config,get_prompt
config=get_config()
prompt_config=get_prompt()["laughing_dog"]

from interface.decisionInterface import decisionInterface
from interface.aiBridgeInterface import aiBridgeInterface

class decision(decisionInterface):
    def __init__(self,gpt_instance:aiBridgeInterface):
        self.gpt_instance=gpt_instance

    def make_decision(self, observation:pd.DataFrame,memory:str,dialog:str)->dict:
        '''
        observation is csv(df) format with columns of:
        Name,Handle,Timestamp,Verified,Content,Comments,Retweets,Likes,Analytics,Tags,Mentions,Emojis,Profile Image,Tweet Link,Tweet ID
        
        return format:
        {
            "target_tweet_id": "target_tweet_id here",
            "action": "reply",
            "content": "content here"
        }
        '''
        observation_filtered = observation[['Name','Handle','Content','Verified','Content','Comments','Retweets','Likes','Analytics','Tags','Mentions','Tweet ID']]
        prompt_input=f"```\n{observation_filtered.to_string()}\n```\n\n{prompt_config['user']}"
        res_gpt_json=self.gpt_instance.call_llm(prompt_system=prompt_config['system'],prompt_user=prompt_input)
        return self.parse_decision(res_gpt_json)
    
    def parse_decision(self,decision:str)->dict:
        return json.loads(decision)
        
    

if __name__ == '__main__':
    import pandas as pd
    from  src.gpt import gpt
    observation=pd.read_csv('tweets/observation_test.csv')
    gpt_instance=gpt()
    decision_instance=decision(gpt_instance)
    res=decision_instance.make_decision(observation=observation,memory='memory',dialog='dialog')
    print(res)
    

