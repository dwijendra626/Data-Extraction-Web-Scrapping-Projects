import requests
import pymongo
import pandas as pd
from bs4 import BeautifulSoup

questionlist = [{}]

DB_NAME = "stackoverflow"
connection_url = 'mongodb://localhost:27017/'

client = pymongo.MongoClient(connection_url)

dataBase = client[DB_NAME]
COLLECTION_NAME = "stackoverflow_questions"
collection = dataBase[COLLECTION_NAME]

def getQuestions(tag,page):
        stackoverflow_url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={page}&pagesize=15'
        r = requests.get(stackoverflow_url)
        soup = BeautifulSoup(r.text,'html.parser')

        questions = soup.find_all('div', {'class' : 'question-summary'})
        for item in questions:
            question = {
                'tag' : tag,
                'title' : item.find('a', {'class' : 'question-hyperlink'}).text,
                'link' : 'https://stackoverflow.com' + item.find('a', {'class': 'question-hyperlink'})['href'],
                'votes' : int(item.find('span', {'class': 'vote-count-post'}).text),
                'date' : item.find('span', {'class': 'relativetime'})['title']
            }
            questionlist.append(question)
        return

for x in range(1,2):
    getQuestions('python', x)
    getQuestions('flask', x)

rec = collection.insert_many(questionlist)








# df = pd.DataFrame(questionlist)
# df.to_csv('stackquestions.xlsx', index=False)
# print('Fin.')

