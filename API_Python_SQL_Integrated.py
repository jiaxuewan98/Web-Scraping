#!/usr/bin/env python
# coding: utf-8

import requests
import bs4
import json
import mysql.connector
import time
import re
user_agent = {'User-agent': 'Mozilla/5.0'}
mykey='be3d20cc' #The key I requested from omdbapi.com personally.


#1-a
#The url to search for all the movies containg the word 'blade':
# http://www.omdbapi.com/?apikey=be3d20cc&s=blade

#1-b
url='http://www.omdbapi.com/?apikey=be3d20cc&s=blade&plot=short&r=json' #The target url
result=requests.get(url,headers=user_agent) #Request the target url
text=result.text
json_data=json.loads(text) #Parse the JSON string to a python JSON object.
print(json.dumps(json_data,indent=2)) #Pretty-print the data.


#1-c
#Iterate through the search results list and print the imdbID out.
for movie in json_data['Search']:
    print(movie['imdbID'])


#2-d
#Python uses the module mysql-connector to connect mysql database.
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root"
)


#Cursor is used to execute SQL queries.
mycursor = mydb.cursor()


#Create a database called 'ucdavis'
create_database='CREATE DATABASE if not exists ucdavis;'
mycursor.execute(create_database)


#Reconnect, using the database ucdavis we just created.
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database='ucdavis'
)
mycursor = mydb.cursor()


#Create a table called 'omdb_test' with the needed columns.
create_table='CREATE TABLE if not exists omdb_test (imdb_id VARCHAR(15) PRIMARY KEY, title VARCHAR(255),year INT(4));'
mycursor.execute(create_table)


#3 To prepare for insertion, let's create the table first.
drop_table='DROP TABLE IF EXISTS omdb;'#In case we need to  re-edit table details.
mycursor.execute(drop_table)
create_table='CREATE TABLE omdb (title VARCHAR(255),year INT(4),genre VARCHAR(255),director VARCHAR(255),imdb_rating INT,rotten_tomatoes INT,metacritic INT,plot VARCHAR(255),box_office VARCHAR(255));'
mycursor.execute(create_table)


#3-a
#The list of our favorite movie titles.
movie_list=['Dunkirk','Frozen','Inception','Avatar','Spotlight','Birdman','Lincoln','Hugo','Moonlight','Arrival']


#Iterate through the movie list. In each iteration, search for the target movie title and extract IMDB ID from the result. Use the IMDB ID to get details and store in database.
for movie in movie_list:
    url='http://www.omdbapi.com/?apikey=be3d20cc&s='+movie #The target url of our target movie.
    time.sleep(1)
    result=requests.get(url,headers=user_agent) #Request the target url
    text=result.text
    json_data=json.loads(text)
    imdbid=json_data['Search'][0]['imdbID'] #Extract the IMDB ID.
    print('Movie:'+movie+', IMDB ID: '+imdbid)
    url='http://www.omdbapi.com/?apikey=be3d20cc&i='+imdbid #The target url using imdbID.
    time.sleep(1)
    result=requests.get(url,headers=user_agent) #Request the target url
    text=result.text
    json_data=json.loads(text) #The movie details.
    print(json.dumps(json_data,indent=2))
    #Extract the movie details.
    title=json_data['Title']
    year=json_data['Year']
    genre=json_data['Genre']
    director=json_data['Director']
    #Parse the ratings to be full grades.
    imdb_rating=float(json_data['imdbRating'])*10
    tomato=re.findall('(\d+)%',json_data['Ratings'][1]['Value'])[0]
    metacritic=re.findall('(\d+)/100',json_data['Ratings'][2]['Value'])[0]
    plot=json_data['Plot']
    box=json_data['BoxOffice']
    #Store the movie details.
    insert= "INSERT INTO omdb VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    val=(title,year,genre,director,imdb_rating,tomato,metacritic,plot,box)
    mycursor.execute(insert, val)
    mydb.commit()

