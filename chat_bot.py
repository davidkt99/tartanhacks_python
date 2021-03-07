#Importing modules
import time
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

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




while (True):
    result = firebase.get('/toPython', 'message')
    user_input = result
    print(user_input)
    if (user_input == 'quit'):
        break
    response = Moti.get_response(user_input)
    output = {
    'message': str(response),
    }
    result = firebase.put('/fromPython', 'log', output)
    print(output)
