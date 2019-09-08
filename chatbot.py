#Importing libraries
import numpy as np
import tensorflow as tf
import re
import time

#Importing dataset
lines = open('movie_lines.txt', encoding ='utf-8',errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding ='utf-8',errors='ignore').read().split('\n')

#Creating a dictionary that maps each line ans its id
id2line = {}
for line in lines:
    li = line.split(' +++$+++ ')
    if len(li) == 5:
        id2line[li[0]] = li[4]

#Creating a list of all conversations
conversations_ids = []
for conversation in conversations[:-1]:
    conv = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","") #refer 7
    conversations_ids.append(conv.split(','))
    
#Separating questions and answers
questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])

#Initial cleaning of data
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm","i am",text)
    text = re.sub(r"he's","he is",text)
    text = re.sub(r"she's","she is",text)
    text = re.sub(r"that's","that is",text)
    text = re.sub(r"what's","what is",text)
    text = re.sub(r"where's","where is",text)
    text = re.sub(r"\'ll","will",text)
    text = re.sub(r"\'re","are",text)
    text = re.sub(r"\'d","would",text)
    text = re.sub(r"won't","will not",text)
    text = re.sub(r"can't","can not",text)
    text = re.sub(r"[-()\"#/@;:<>{}+=?,]","",text)
    return text            

#Cleaning questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
         
#Cleaning answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))    
    
#Creating a dictionary that maps each word to its number of occurances
word2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word2count :
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for question in clean_answers:
    for word in answer.split():
        if word not in word2count :
            word2count[word] = 1
        else:
            word2count[word] += 1
            
#Creating two dictionaries that map the question words to a unique integer
#Tokenization and filtering the non frequent words
