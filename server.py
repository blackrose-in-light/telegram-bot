import os,requests,time
from dotenv import load_dotenv

# get env variables
load_dotenv('./.env')
token = os.getenv('TOKEN')
endpoint = os.getenv('ENDPOINT')

#  telegram bot class
class TelegramBot:
    # variable initialization
    def __init__(self,token,endpoint):
        self.token = token
        self.endpoint = endpoint
        self.last_message = None

    # get last message 
    def get_last_message(self):
        url = self.endpoint + 'bot' + self.token + '/getUpdates'
        res = requests.get(url)
        self.last_message = dict(res.json()['result'][-1])
        return

    # reply dictionary
    def message_reply(self,msg,usr):
        switch={
        'hi':'Hello {}'.format(usr),
        'hello':'Hi {}'.format(usr),
        'how are you':'Iam good, What about you?',
        'iam good':'Great',
        'good':'Great',
        '/start':'How Can I Help You?',
        'sing a song for me':'Oops!! May be later!',
        'good morning':'Good Morning',
        'good afternoon':'Good Afternoon',
        'good night':'Good Night',
        'bye':'See You'
        }
        return switch.get(msg.lower(),"Sorry I didn't get it!")

    # send message
    def send_message(self,user_id,message):
        url = self.endpoint + 'bot' + self.token + '/sendMessage'
        payload = {
            'chat_id':user_id,
            'text':message
        }
        requests.post(url,payload)
        return

    # bot actions
    def bot_actions(self):
        self.get_last_message()
        last_update_id = self.last_message['update_id']
        time.sleep(1)
        while True:
            self.get_last_message()
            curr_update_id = self.last_message['update_id']
            if self.last_message != None:
                if last_update_id != curr_update_id:
                    user_text = self.last_message['message']['text']
                    user_name = self.last_message['message']['from']['first_name']
                    user_id = self.last_message['message']['from']['id']
                    reply = self.message_reply(user_text,user_name)
                    self.send_message(user_id,reply)
                    last_update_id += 1
                    print('{} : {}'.format(user_name,user_text))
                    print('{} : {}'.format('bot',reply))
            else:
                print('No Message Here')
            time.sleep(1)
    
# telegram instance
tg_bot = TelegramBot(token,endpoint)
tg_bot.bot_actions()