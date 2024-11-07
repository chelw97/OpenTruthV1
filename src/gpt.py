import os
import sys
from openai import OpenAI
sys.path.append(os.path.abspath('.'))

from interface.aiBridgeInterface import aiBridgeInterface
from src.config import get_config,get_credentials
config=get_config()
credentials=get_credentials()


class gpt(aiBridgeInterface):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=credentials['OPENAI_API_KEY'])

    def call_llm(self,prompt_system,prompt_user,response_format='json'):
        # Define the messages for the conversation
        messages = [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]

        if response_format=='json':
             # Create the chat completion
            completion = self.client.chat.completions.create(
                model=config['llm_settings']["gpt"]["model"],
                messages=messages,
                max_tokens=config['llm_settings']["gpt"]["max_tokens"],
                temperature=config['llm_settings']["gpt"]["temperature"],
                top_p=config['llm_settings']["gpt"]["top_p"],
                frequency_penalty=config['llm_settings']["gpt"]["frequency_penalty"],
                presence_penalty=config['llm_settings']["gpt"]["presence_penalty"],
                n=1,
                response_format={"type": "json_object"}
            )
        else:
            # Create the chat completion
            completion = self.client.chat.completions.create(
                model=config['llm_settings']["gpt"]["model"],
                messages=messages,
                max_tokens=config['llm_settings']["gpt"]["max_tokens"],
                temperature=config['llm_settings']["gpt"]["temperature"],
                top_p=config['llm_settings']["gpt"]["top_p"],
                frequency_penalty=config['llm_settings']["gpt"]["frequency_penalty"],
                presence_penalty=config['llm_settings']["gpt"]["presence_penalty"],
                n=1
            )

        # Extract the generated tweet
        res = completion.choices[0].message.content
        return res
        

if __name__ == "__main__":
    gpt_instance=gpt()
    prompt_user= '''
```
contnet here
```

you are viewing your twitter homepage with the content above. You can do the following actions:

like: like a tweet
Quote: Quote a tweet and post
Reply: reply a tweet
Post: post one tweet

please decide the action you want to do in json format like:

{
    "target_tweet_id":"target_tweet_id here",
    "action": "reply",
    "content": "you contetn here"
}
'''
    res=gpt_instance.call_llm(prompt_system="you are a cute laughing dog who bought some bitcoin and always speak with sarcastic and humorous tone.",prompt_user=prompt_user,response_format="json")
    print(res)