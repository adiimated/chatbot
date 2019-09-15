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
threshold = 20
questionswords2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1

answerswords2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1        

#Adding the last tokens to these two dictionaries
#Tokenization is the process of tokenizing or splitting a string, text into a list of tokens.
#One can think of token as parts like a word is a token in a sentence, and a sentence is a token in a paragraph.
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']
for token in tokens:
    questionswords2int[token] = len(questionswords2int) + 1                     #refer 13
for token in tokens:
    answerswords2int[token] = len(answerswords2int) + 1
    
#Creating the inverse dictionary of the answerswords2int dictionary 
#Required in creating seq2seq model
answersints2word = {w_i:w for w,w_i in answerswords2int.items()}                #refer 14

#Adding the end of string token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
#To denote end of answer[end of string]
    
#Translating all the questions and the answers into integers
#And replacing all the words that were filtered out by <OUT>
questions_into_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_into_int.append(ints)
    
answers_into_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)

#Sorting questions and answers by the lenghth of the question            
#Speeds up the training and optimize it
#Reduces padding during the training   #Refer 17 
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1,25 + 1):
    for i in enumerate(questions_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_into_int[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])
            

#Creating placeholders for inputs and the targets
#A placeholder is simply a variable that we will assign data to at a later date. 
#It allows us to create our operations and build our computation graph, without needing the data. 
#In TensorFlowterminology, we then feed data into the graph through these placeholders.
def model_inputs():
    inputs = tf.placeholder(tf.int32,[None,None],name = 'input')
    targets = tf.placeholder(tf.int32,[None,None],name = 'target')
    lr = tf.placeholder(tf.float32,name = 'learning_rate')
    keep_prob = tf.placeholder(tf.float32,name = 'keep_prob')
    return inputs,targets,lr,keep_prob


            

