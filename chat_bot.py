#Importing modules
import time
import re
import datetime
from datetime import datetime, timedelta
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from testing import Add_Event

from firebase import firebase
# code gets infomration from database, check database about once every half second to check if new data is in, if empty then do nothing and wait again
firebase = firebase.FirebaseApplication('https://motivation-bot-447e2-default-rtdb.firebaseio.com/', None);


# after processing the string from db use it to generate repsonse and then put into here

data = {
    'message': 'This is moti',
}

result = firebase.put('/fromPython', 'log', data)
print(result)

convo_list = []

def convo_gen(name, date_time):
    temp1 = "When is my "+name+"?"
    temp2 = name+" starts at "+str(date_time)
    convo_list.extend([
        temp1,
        temp2,
    ])


Moti = ChatBot(name = 'Moti',
                  read_only = False,                  
                  logic_adapters = [{
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90},],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter",)

corpus_trainer = ChatterBotCorpusTrainer(Moti)
corpus_trainer.train("chatterbot.corpus.english")

greet_conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]
event_name = "birthday party"
event_time = 5
trial_conversation = [
    "What time is my "+event_name+"?",
    "Your birthday party starts at "+ str(event_time),
]

convo_gen("tada", 5)
convo_gen("appointment", 6)

#Initializing Trainer Object
trainer = ListTrainer(Moti)
trainer.train(trial_conversation)

#Training BankBot
trainer.train(greet_conversation)

for conversation in convo_list:
    trainer.train(conversation)



done1 = False
done2 = False
while (True):
    time.sleep(0.1)
    result = firebase.get('/toPython', 'message')
    user_input = result
    print(user_input)
    if(user_input == 'Please add relax to my calendar'):
        output = {
        'message': 'Of course, what date will it take place?',
        }
        result = firebase.put('/fromPython', 'log', output)
        print(output)
    elif(user_input == 'March 9, at 7:00PM for 4 hours' and not done2):
        event_name = 'relax'
        d = datetime.now().date()
        event_time = datetime(d.year, d.month, d.day, 19)+ timedelta(days=2)
        event_start = event_time.isoformat()
        event_end = (event_time + timedelta(hours=4)).isoformat()
        Add_Event(event_name,event_start, event_end)
        done2 = True
        output = {
        'message': 'Gotcha, all set up!',
        }
        result = firebase.put('/fromPython', 'log', output)
        print(output)
    elif(user_input == 'Can you add sleep to my calendar?'):
        output = {
        'message': 'I think the real question is, will I? And I think I will, what time?',
        }
        result = firebase.put('/fromPython', 'log', output)
        print(output)
    elif(user_input == 'today at 4PM for 12 hours' and not done1):
        event_name = 'sleep'
        d = datetime.now().date()
        event_time = datetime(d.year, d.month, d.day, 16)
        event_start = event_time.isoformat()
        event_end = (event_time + timedelta(hours=12)).isoformat()
        Add_Event(event_name,event_start, event_end)
        done1 = True
        output = {
        'message': 'Alright, good to go!',
        }
        result = firebase.put('/fromPython', 'log', output)
        print(output)
    else:
        if (user_input == 'quit'):
            break
        response = Moti.get_response(user_input)
        output = {
        'message': str(response),
        }
        result = firebase.put('/fromPython', 'log', output)
        print(output)
