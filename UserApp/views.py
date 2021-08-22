from django.shortcuts import render, redirect
from .models import User_Data
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
#import simplejson as json
from django.views.decorators.csrf import csrf_exempt
import json
import time
from Recommendation.models import Recommended_Data
import re
from bs4 import BeautifulSoup
import pickle
from operator import itemgetter
import numpy as np
import ast
from scipy import spatial


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def tokenization(sentance) :
    sentance = re.sub(r"http\S+", "", sentance)
    sentance = BeautifulSoup(sentance, 'lxml').get_text()
    sentance = decontracted(sentance)
    sentance = ' '.join(e.lower() for e in sentance.split() )
    sentance.strip()
    return sentance

def word_embeddings(vector,keys ,sent) :
    
    sent_vec = np.zeros(100) 
    cnt_words =0 
    for word in sent: 
        if word in keys:
            vec = word
            sent_vec += vector[vec]
            cnt_words += 1
    if cnt_words != 0:
        sent_vec /= cnt_words
    return sent_vec


with open('machine_learning\word_embeddings(100).pickle', 'rb') as handle:
    embedding_vector = pickle.load(handle)


with open('machine_learning\word_keys(100).pickle', 'rb') as handle:
    word_keys = pickle.load(handle)


API_KEY = 'b0ed4f29b4d146c29c9f79b25df6b404'

# Create your views here.



def home(request):
	#Most Viewed
	url = f'https://newsapi.org/v2/everything?domains=wsj.com&language=en&apiKey={API_KEY}'
	response = requests.get(url)
	print(response)
	data  =response.json()
	print("Hello")
	articles = data['articles']

	#top_headlines

	query =	{'source':'bbc-news',"sortBy": "top","apiKey": API_KEY }
	main_url = " https://newsapi.org/v1/articles"
	response = requests.get(main_url, params=query)
	data = response.json() 
	art_tesla = data["articles"]

	#Trending News
	url_trending = f'https://newsapi.org/v2/top-headlines?language=en&sources=techcrunch&apiKey={API_KEY}'
	response = requests.get(url_trending)
	trending = response.json()
	art_trending = trending['articles']
	#sports
	url_sports = f'https://newsapi.org/v2/top-headlines?language=en&category=sports&apiKey={API_KEY}'
	response = requests.get(url_sports)
	sports = response.json()
	sports_trending = sports['articles']
	#Technology
	url_technology = f'https://newsapi.org/v2/top-headlines?language=en&category=technology&apiKey={API_KEY}'
	response = requests.get(url_technology)
	technology = response.json()
	technology = technology['articles']
	#Business
	url_business = f'https://newsapi.org/v2/top-headlines?language=en&category=business&apiKey={API_KEY}'
	response = requests.get(url_business)
	business = response.json()
	business = business['articles']
	#Entertainment
	url_entertainment = f'https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey={API_KEY}'
	response = requests.get(url_entertainment)
	entertainment = response.json()
	entertainment = entertainment['articles']

	return render(request, 'index.html',{'data':articles,'art_tesla':art_tesla,'trending': art_trending,'sports':sports_trending,'technology':technology,'business':business,'entertainment':entertainment})

@login_required(login_url='/user/login/') 

def news_api(request):
	#url = f'https://newsapi.org/v2/everything?q=Apple&from=2021-04-20&sortBy=popularity&apiKey={API_KEY}'
	uobj=request.user
	
	interest_list = ['Business', 'Entertainment', 'General', 'Health', 'Science','Sports','Technology']

	try:
		category = request.GET.get('category')
	except:
		category=None
	try:
		top_news = request.GET.get('top_news')
	except:
		top_news= None
	try:
		top_headlines = request.GET.get('top_headlines')
	except:
		top_headlines= None
	if top_news:
		query =	{'source':'bbc-news',"sortBy": "top","apiKey": API_KEY }
		main_url = " https://newsapi.org/v1/articles"
		response = requests.get(main_url, params=query)
		data = response.json() 
		articles = data["articles"]
		category = 'Top News'
	elif top_headlines:
		url = f'https://newsapi.org/v2/top-headlines?language=en&country=us&apiKey={API_KEY}'
		response = requests.get(url)
		data = response.json() 
		articles = data["articles"]
		category = 'Top Headlines'
	elif category:
		
		url = f'https://newsapi.org/v2/top-headlines?language=en&category={category}&apiKey={API_KEY}'
		response = requests.get(url)
		data = response.json() 
		articles = data['articles']

		

	else:
		url = f'https://newsapi.org/v2/top-headlines?language=en&category={interest_list[0]}&apiKey={API_KEY}'
		response = requests.get(url)
		data = response.json()
		articles = data['articles']
		category = interest_list[0]

	return render(request,'news_api.html',{'data':articles,'category':category, 'interest_list':interest_list})


def single_page(request):
	single_url = request.GET.get('single_url')
	single_title = request.GET.get('single_title')
	single_img = request.GET.get('single_img')
	single_description = request.GET.get('single_description')
	single_content = request.GET.get('single_content')
	#print("Single Description :::",single_description)


	#data = [single_url, single_title, single_img, single_description, single_content]
	context = {'url':single_url, 'title':single_title,'img':single_img, 'desc':single_description, 'content':single_content}
	#print("The Data is :\n",data)
	
	return render(request, 'single3.html',{'data':context})




@csrf_exempt
@login_required(login_url='/user/login/') 

def interest(request):
	li=[]
	url=""
	#User_Data=User_Data(self)
	uobj=request.user
	if request.method=='POST':
		it1=request.POST['ckb1']
		if it1!=" ":
			li.append(it1)
		it2=request.POST['ckb2']
		if it2!=" ":
			li.append(it2)
		it3=request.POST['ckb3']
		if it3!=" ":
			li.append(it3)
		it4=request.POST['ckb4']
		if it4!=" ":
			li.append(it4)
		it5=request.POST['ckb5']
		if it5!=" ":
			li.append(it5)
		it6=request.POST['ckb6']
		if it6!=" ":
			li.append(it6)
		it7=request.POST['ckb7']
		if it7!=" ":
			li.append(it7)

		if len(li)>3 or len(li)<3:
			return HttpResponse('<script>alert("Select Only 3 interest");window.location="%s"</script>'%url)
		elif len(li)==3:
			#print("THe interested are in list :",li)
			listToStr = ' '.join(map(str, li))
			Recommended_Data.objects.filter(user=uobj).update(interest=listToStr)
			return redirect('/user/news/')

		
	return render(request, 'interest.html')

def signup_call(request):
	if request.method=='POST':
		email=request.POST['email']
		uname=request.POST['username']
		passwd=request.POST['password']
		c_passwd=request.POST['c_password']
		url='/user/signup/'
		try:
			print("#First line")
			u=User_Data(email=email,username=uname,
				password=passwd,c_password=c_passwd)
			print(u)
			u.save()
			#print("2")
			newuser = User(email=email,username=uname,password=make_password(passwd))
			#print(newuser)
			newuser.save()
			current_user = authenticate(username=uname, password=passwd)
			u = current_user
			#Changed
			
			p = Recommended_Data(user=u)
			p.save()
			
			return redirect('/user/login/')
		except:
			return HttpResponse('<script>alert("Username already exists..");\
                    window.location="%s"</script>'%url)
		return redirect('/signup/')
	return render(request,'signup.html')
def login_call(request):
	if request.method=='POST':
		uname=request.POST['username']
		passwd=request.POST['password']
		url=''
		try:
			current_user = authenticate(username=uname, password=passwd)
			
			if current_user:
				if current_user.last_login==None:
					login(request, current_user)
					return redirect('/user/interest/')
				else:
					login(request,current_user)
					print(current_user.last_login)
					return redirect('/user/news/')
			else:
				return HttpResponse('<script>alert("wrong password or username");window.location="%s"</script>'%url)
		except:
			return HttpResponse('<script>alert("wrong password or username");window.location="%s"</script>'%url)
	return render(request, 'login.html')
	
def logout_call(request):
	logout(request)
	return redirect('/user/login/')




def timesp(request):
	#print('came')
	uobj=request.user
	
	
	if request.method=='POST':
		naa=request.POST['na']
		#print(naa," sec")
		time_spent = float(naa)
		print(time_spent)
		#time is in second
		title = request.POST['title']
		print(title)
		content = request.POST['content']
		print(content)
		url = request.POST['url']
		description = request.POST['desc']
		print(description)
		text = str(title) + " " + str(content) + " " + str(description)
		print(text)
		text = tokenization(text)
		vector= word_embeddings(embedding_vector,word_keys,text.split()) 
		print(vector)
		print(url)
		no_of_words= len(text.split())
		rating= time_spent/no_of_words
		 
		v1 = vector*rating
		
		l = []
		for x in v1 :
			l.append(x)
		print(l)
		
		uobj=request.user
		data = Recommended_Data.objects.get(user=uobj)
		vfromdatabase = data.user_vector
		print(vfromdatabase)
		if vfromdatabase == "nthg" :
			s  = str(l)
			# print("v1",l)
			Recommended_Data.objects.filter(user=uobj).update(user_vector = s)
			print("first_activity")
		else : 
			print("vfromdatabase")
			print(vfromdatabase)
			previous_vector = ast.literal_eval(vfromdatabase)
			res_v = []
			for i in range(0, 100):
				res_v.append(previous_vector[i] + l[i])
			
			print("final_vector",res_v)
			Recommended_Data.objects.filter(user=uobj).update(user_vector = res_v)
			print("not_first")

	return redirect('/user/news')