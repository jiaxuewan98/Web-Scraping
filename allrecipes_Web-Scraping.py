#!/usr/bin/env python
# coding: utf-8

import requests
import bs4
import time
import re
from collections import Counter
url='https://www.thyssenkrupp-elevator.com/kr/products/multi/' #The target url.
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'} #Set up the user_agent.


#1-a
response=requests.get(url,headers = user_agent) #Request the html.
#1-b
file=open('elevator.htm','w',encoding='utf-8') #Create a new file using utf-8.
file.write(response.text) #Write the html requested into it.
file.close()


#1-c
file=open('elevator.htm','r',encoding='utf-8')
page=file.read()# Read the file in plain txt.
file.close()


#1-d
newpage=re.sub('<[^>]*>','',page)#Replace all the tags.
print(newpage)


#1-e
#Findall korean characters that appear right before '.'
#\u3131-\uD79D is the utf-8 code range for all Korean characters.
last_characters=re.findall('([\u3131-\uD79D])\.',newpage)
print(last_characters)


#1-f
text_f=''
for c in last_characters:
    text_f=text_f+c
#Counter function creates a dictionary that contains each character in a given string and the count of time it occurs.
characters=Counter(text_f)
max_count=0
max_count_character=0
#Loop through all the characters, for each Korean character, check if it's the most occuring one so far and update the max_count accordingly.
for character in characters:
    if characters[character]>max_count:
        max_count=characters[character]
        max_count_character=character
print('The most occuring Korean character is '+max_count_character+', and it occured '
      +str(max_count)+' times.')


#2-a
signin_url='https://www.allrecipes.com/account/signin/' #The url to sign in.
time.sleep(10) #Hold ten seconds before next scrape. 
response=requests.get(signin_url,headers = user_agent) #Request the html.
soup=bs4.BeautifulSoup(response.text)


#Locate the token needed for log in
token=soup.find('input',{'name':'SocialCsrfToken'})['value']


#These form data can be found in the 'Network' of browser when logging in to the page.
keys={
    'ReferringUrl':'https://www.allrecipes.com/',
    'AuthLayoutMode':'Standard',
    'SocialCsrfToken':token,
    'txtUserNameOrEmail':'hdzhang@ucdavis.edu',
    'password':'Ricardoddr',
    'RememberMe':'on'
}


#Create a session object. Python uses the object called 'session' to handle web log-in and cookies stuff.
session_requests=requests.session()
time.sleep(10) #Hold ten seconds before next scrape. 
result=session_requests.post(signin_url,
                             data=keys,
                             headers=user_agent
)
#Now 'result' would be the web page after successfully login.


#2-b
soup=bs4.BeautifulSoup(result.text)
print(soup.find('span',{'class':'username'}).text)#Find my own user name. It proves that I've successfully logged in.

