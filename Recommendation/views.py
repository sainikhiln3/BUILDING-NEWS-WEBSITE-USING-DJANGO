from django.shortcuts import render, redirect
from .models import Recommended_Data
from django.contrib.auth.models import User
from UserApp.models import User_Data
import requests
from .vectorization import decontracted,tokenization,word_embeddings

import re
from bs4 import BeautifulSoup
import pickle
from operator import itemgetter
import numpy as np
import ast
from scipy import spatial

API_KEY = 'b0ed4f29b4d146c29c9f79b25df6b404'

# Create your views here.


with open('machine_learning\word_embeddings(100).pickle', 'rb') as handle:
    embedding_vector = pickle.load(handle)


with open('machine_learning\word_keys(100).pickle', 'rb') as handle:
    word_keys = pickle.load(handle)


def home(request):
	uobj=request.user
	data1 = Recommended_Data.objects.get(user=uobj)
	vfromdatabase = data1.user_vector
	if vfromdatabase == "nthg" : # user havent created any activity
		intrest = data1.interest
		interest_list = list(intrest.split(" "))
		print(interest_list) # only 3 artciles 
		cat_1={}
		cat_2={}
		cat_3={}
		for cat in interest_list:
			url = f'https://newsapi.org/v2/top-headlines?language=en&category={cat}&apiKey={API_KEY}'
			response = requests.get(url)
			data = response.json() 
			articles = data['articles']
			
			print()
			
			if cat == interest_list[0]:
				f1 = articles[0]
				cat_1 = {'title':f1['title'],'description':f1['description'],'content':f1['content'],'url':f1['url'],'urlToImage':f1['urlToImage']}


			elif cat == interest_list[1]:
				f2 = articles[0]
				print(cat)
				cat_2 = {'title':f2['title'],'description':f2['description'],'content':f2['content'],'url':f2['url'],'urlToImage':f2['urlToImage']}

			
			elif cat == interest_list[2]:
				f1 = articles[0]
				cat_3 = {'title':f1['title'],'description':f1['description'],'content':f1['content'],'url':f1['url'],'urlToImage':f1['urlToImage']}
				
		
		c1=[]
		c2=[]
		c3=[]
		c1.append(cat_1)
		c2.append(cat_2)
		c3.append(cat_3)


		return render(request,'recommendation1.html',{'cat_1':c1,'cat_2':c2,'cat_3':c3})
	else :
		# recommendation based on user vector 
		# l == 10 artciles ids 

		url = f'https://newsapi.org/v2/top-headlines?language=en&country=us&apiKey={API_KEY}'
		response = requests.get(url)
		data = response.json() 
		articles = data["articles"]
		
		# print(articles)
		# print(len(articles))
		# print(articles[0].keys())
		a = []
		v = []
		for x in articles :
			text = str(x["title"]) + " " + str(x["content"]) + " " + str(x["description"])
			# print(text)
			a.append(x)
			text = tokenization(text)
			vector= word_embeddings(embedding_vector,word_keys,text.split())
			c = []
			for p in vector :
				c.append(p)
			v.append(c)
		vector1 = ast.literal_eval(vfromdatabase)
		d= []
		i = 0
		for k in v :
			vector2 = np.array(k)
			value= 1 - spatial.distance.cosine(vector1,vector2)
			#print("3")
			d.append((value,a[i]))
			i = i+1
		b = sorted(d)  # https://www.geeksforgeeks.org/python-sort-tuples-increasing-order-key/
		recommended_artciles = [b[-1][1],b[-2][1],b[-3][1]]
		# scores = [b[-1][0],b[-2][0],b[-3][0]]
		# print(b)
		# print("@@@@@@@@@")
		# print(recommended_artciles)
		# print(scores)
		return render(request,'recommendation.html',{'recommended_artciles':recommended_artciles})
