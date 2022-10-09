from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Properties
from joblib import load
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dataframe_image as dfi
from . models import Sell

regressor = load('./savedmodels/models.joblib')
from .models import sp
# Create your views here.
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            
            return redirect('index')
        else:
            messages.info(request,'invalid ceredentials')
            return redirect('/')
    else:
        return render(request, 'login.html')


def register(request):

    if  request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
            user.save()
            print('welcome',user.first_name)
            return redirect('login')
    else:
        return render(request, 'register.html')
def home(request):
    if request.method == 'POST':
        superarea = request.POST['superarea']
        ppsqft = request.POST['ppsqft']
        carpetarea = request.POST['carpetarea']
        
        y_pred = regressor.predict([[superarea,ppsqft,carpetarea]])
        print(y_pred)
        print('here it is')
        return render(request, 'index.html', {'result' : y_pred})
    else:
        return render(request, 'index.html')
def properties(request):
    if request.method == 'POST':
        searchh = sp.objects.all()
        searchh.address = request.POST.get('address')
        searchh.mintotprice = int(request.POST.get('mintotprice'))
        searchh.maxtotprice = int(request.POST.get('maxtotprice'))
        searchh.minsuperarea = int(request.POST.get('minsuperarea'))
        searchh.maxsuperarea =int(request.POST.get('maxsuperarea'))
        print('got the values')
        print(searchh.mintotprice)
        props=Properties.objects.filter(totprice__gte=searchh.mintotprice,totprice__lt=searchh.maxtotprice,Superarea__gte=searchh.minsuperarea,Superarea__lt=searchh.maxsuperarea).values()
        return render(request,'properties.html',{'props':props})
    else:
        return render(request,'properties.html')
def analysis(request):
    if request.method == 'POST':
        cuisine = request.POST['cuisine']
        print(cuisine)
        df = pd.read_csv('C:/Users/soham/Downloads/Zomato_Mumbai_Dataset.csv',delimiter='|')
        wrong_data = df['PAGE NO'] == 'PAGE NO'
        df[wrong_data]
        df = df[~wrong_data]
        df.drop(['URL', 'PAGE NO', 'CITY','TIMING'], axis = 1, inplace=True)
        df = df.drop(labels=15080, axis=0)
        df.fillna('NA', inplace=True)
        df['RATING'].replace(to_replace=['-','NEW','Opening'], value='0', inplace=True)
        df['VOTES'].replace(to_replace=['-','NEW','Opening'], value='0', inplace=True)
        df['PRICE'] = df['PRICE'].astype('int64')
        df['RATING'] = df['RATING'].astype('float64')
        df['VOTES'] = df['VOTES'].astype('int64')
        useless_data = (df['RATING'] == 0.0) | (df['VOTES'] == 0)
        df[useless_data]
        df = df[~useless_data]
        df['RATING_TYPE'].replace(to_replace='Excelente' , value='Excellent', inplace=True)
        df['RATING_TYPE'].replace(to_replace=['Veľmi dobré','Bardzo dobrze','Muy Bueno','Velmi dobré'] , value='Very Good', inplace=True)
        df['RATING_TYPE'].replace(to_replace=['Skvělá volba','Dobrze','Bueno','Buono','Dobré','Bom','Skvělé'] , value='Good', inplace=True)
        df['RATING_TYPE'].replace(to_replace=['Priemer','Média','Çok iyi'] , value='Average', inplace=True)
        df['RATING_TYPE'].replace(to_replace=['Průměr','Promedio','Ortalama','Muito Bom','İyi'] , value='Poor', inplace=True)
        df['RATING_TYPE'].replace(to_replace=['Baik','Biasa','Media','Sangat Baik'] , value='Very Poor', inplace=True)
        df['REGION'] = df['REGION'].str.replace('[a-zA-Z].+-- ','',regex=True)
        df['REGION'] = df['REGION'].str.replace(' west', 'West',regex=True)
        df['REGION'] = df['REGION'].str.replace(' east', 'East',regex=True)
        df['REGION'] = df['REGION'].str.replace('4 Bungalows|7 Andheri|Azad Nagar|Near Andheri Station|Near Andheri West Station|Veera Desai Area','Andheri West',regex=True)
        df['REGION'] = df['REGION'].str.replace('Mahakali|Chakala|Near Andheri East Station','Andheri East', regex=True)
        df['REGION'] = df['REGION'].str.replace('Bandra Kurla Complex','Bandra West',regex=True)
        df['REGION'] = df['REGION'].str.replace('CBD-Belapur','CBD Belapur',regex=True)
        df['REGION'] = df['REGION'].str.replace('Girgaon Chowpatty','Chowpatty',regex=True)
        df['REGION'] = df['REGION'].str.replace('Dadar Shivaji Park','Dadar',regex=True)
        df['REGION'] = df['REGION'].str.replace('Flea Bazaar Café|Kamala Mills Compound','Lower Parel',regex=True)
        df['REGION'] = df['REGION'].str.replace('Runwal Green','Mulund',regex=True)
        df['REGION'] = df['REGION'].str.replace('Mumbai CST Area','Mumbai Central',regex=True)
        df['REGION'] = df['REGION'].str.replace('Kopar Khairane|Seawoods|Turbhe|Ulwe','Navi Mumbai',regex=True)
        df['REGION'] = df['REGION'].str.replace('New Panvel|Old Panvel','Panvel',regex=True)
        df['REGION'] = df['REGION'].str.replace('Kamothe','Sion',regex=True)
        df['REGION'] = df['REGION'].str.replace('Ghodbunder Road|Majiwada','Thane West',regex=True)
        df[df.duplicated()]
        df = df.drop_duplicates()
        df.head()
        fig = px.histogram(df, x='CUSINE TYPE', color='CUSINE TYPE', 
             title= 'No. of Restaurants by Cuisine Type', 
             labels={'CUSINE TYPE':'Cuisine Type'})
        #fig.write_image("C:/Users/soham/ipd/ipd/static/images/firstgraph.png")
        y=fig.show()
        rating_type_df = df['RATING_TYPE'].value_counts().reset_index()
        rating_type_df.rename(columns={'index':'RATING TYPE', 'RATING_TYPE':'COUNT OF RESTAURANTS'}, inplace=True)
        
        #dfi.export(rating_type_df, 'C:/Users/soham/ipd/ipd/static/images/dataframe1.png')
        
        cuisine_df = df[df['CUSINE_CATEGORY'].str.contains(cuisine)]
        cuisine_df.sort_values(by='RATING',ascending=False).head(10)
        #dfi.export(cuisine_df.sort_values(by='RATING',ascending=False).head(20), 'C:/Users/soham/ipd/ipd/static/images/dataframe2.png')
        highest_rated_df = df[df['RATING'] >= 4.5]
        fig1 = px.histogram(highest_rated_df, x='REGION', color='CUSINE TYPE', 
             title= 'No. of Best Restaurant for each Cuisine Type by Places').update_xaxes(categoryorder="total descending")

        y1=fig1.show()
        highest_rated_price_df = highest_rated_df.groupby(by=['REGION', 'CUSINE TYPE'])['PRICE'].mean().reset_index()
        highest_rated_price_df.head(20)
        #dfi.export(highest_rated_price_df.head(20), 'C:/Users/soham/ipd/ipd/static/images/dataframe3.png')
        fig2 = px.scatter(highest_rated_price_df, x="REGION", y="PRICE", color="CUSINE TYPE", symbol="CUSINE TYPE", 
           title=' Avg Price Distibution of High rated restaurant for each Cuisine Type').update_traces(marker_size=10)

        y2=fig2.show()
        cuisinee_df = df[df['CUSINE_CATEGORY'].str.contains(cuisine)]
        
        #dfi.export(cuisinee_df.head(20), 'C:/Users/soham/ipd/ipd/static/images/dataframe4.png')
        cuisinee1_df = cuisinee_df.groupby(by='REGION').agg({'NAME' : 'count', 'PRICE' : 'mean'}).rename(columns= {'NAME' : 'COUNT OF RESTAURANTS'}).reset_index()
        cuisinee1_df = cuisinee1_df.sort_values('COUNT OF RESTAURANTS', ascending=False).head(25)
        
        #dfi.export(cuisinee1_df.head(20), 'C:/Users/soham/ipd/ipd/static/images/dataframe5.png')
        fig3 = px.bar(cuisinee1_df, x='REGION', y='COUNT OF RESTAURANTS', color='PRICE', title= 'No. of "mentioned cuisine" Restaurants by Places')

        y3=fig3.show()
        price_rating_df = df.groupby(['CUSINE TYPE', 'RATING'])['PRICE'].mean().reset_index()
        price_rating_df1 = df.groupby(['CUSINE TYPE'])['PRICE'].mean().reset_index()
        

        #dfi.export(price_rating_df1.head(30), 'C:/Users/soham/ipd/ipd/static/images/dataframe6.png')
        fig4 = px.line(price_rating_df, y="PRICE", x="RATING",color='CUSINE TYPE')

        y4=fig4.show()
        region_price_df = df.groupby(['REGION'])['PRICE'].mean().reset_index()

        #dfi.export(region_price_df.head(40), 'C:/Users/soham/ipd/ipd/static/images/dataframe7.png')
        fig5 = px.scatter(region_price_df, x="REGION", y="PRICE").update_traces(marker_size=8)

        y5=fig5.show()
        
        region_price_df1 = df.groupby(['CUSINE_CATEGORY','REGION'])['PRICE'].mean().reset_index()
        #dfi.export(region_price_df1.head(40), 'C:/Users/soham/ipd/ipd/static/images/dataframe8.png')
        
        fig6 = px.line(region_price_df1, y="PRICE", x="CUSINE_CATEGORY",color='REGION')

        y6=fig6.show()
        
        return render(request, 'analysis.html',{'y':y,'y1':y1,'y3':y2,'y3':y3,'y4':y4,'y5':y5,'y6':y6})
    else:
        return render(request, 'analysis.html')
def sell(request):
    if request.method == 'POST':
        searchh = sp.objects.all()
        searchh.address = request.POST.get('address')
        searchh.mintotprice = int(request.POST.get('mintotprice'))
        searchh.maxtotprice = int(request.POST.get('maxtotprice'))
        searchh.minsuperarea = int(request.POST.get('minsuperarea'))
        searchh.maxsuperarea =int(request.POST.get('maxsuperarea'))
        print('got the values')
        print(searchh.mintotprice)
        sells=Sell.objects.filter(totprice__gte=searchh.mintotprice,totprice__lt=searchh.maxtotprice,Superarea__gte=searchh.minsuperarea,Superarea__lt=searchh.maxsuperarea).values()
        return render(request,'sell.html',{'sells':sells})
    else:
        return render(request,'sell.html')


    