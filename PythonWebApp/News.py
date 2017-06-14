import requests
import json

import properties

'''
News article object to contain all relevant information from api
'''
class newsArticle:
	imageUrl = ""
	title = ""
	description = ""
	author = ""
	def __init__(self, imageUrl, title, description, author):
		self.imageUrl = imageUrl
		self.title = title
		self.description = description
		self.author= author

'''
Parse the JSON response from api and get relevant information for each source
'''
def pullArticle(articleList, source):
	business = requests.get("https://newsapi.org/v1/articles?source="+source+"&sortBy=top&apiKey="+properties.newsApiKey)
	data = json.loads(business.text)
	source = data['source']
	articles = data['articles']
	article = articles[0]
	imageUrl = article['urlToImage']
	description = article['description']
	title = article['title']
	if article['author'] != None:
		author = source+"- "+article['author']
	else:
		author = source+"- "+"No author"
	newArticle = newsArticle(imageUrl, title, description,author)
	articleList.append(newArticle)
	return articleList


'''
Pull all the news from the three sources
'''
def pullNews():
	articleList = []
	pullArticle(articleList, "business-insider")
	pullArticle(articleList, "ign")
	pullArticle(articleList, "recode")
	return articleList