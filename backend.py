from flask import Flask, render_template, request
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import time 
import os
import requests
from deep_translator import GoogleTranslator 
from nltk .sentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import json
import plotly
import plotly.express as px


app = Flask(__name__)

#driver=webdriver.Edge(os.getcwd()+"\credits.html")
#driver.get("https://www.instagram.com/")

@app.route('/',methods = ['GET'])
def show_index():
    return render_template('index.html')
driver=webdriver.Edge(os.getcwd()+"\credits.html")
driver.get("https://www.instagram.com/")
@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
    Id = request.form['pay']
    Pin = request.form['pass']
    username=driver.find_element(By.NAME,"username")
    username.send_keys(Id)
    password=driver.find_element(By.NAME,"password")
    password.send_keys(Pin)
    driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button').click()
    return render_template('index2.html')

#@app.route('/send_data', methods = ['POST'])
@app.route('/account',methods = ['POST'])
def get_the_account_detail():
    account=request.form["account"]
    search = driver.find_element(By.CLASS_NAME,"_aauy")
    search.send_keys(account)
    time.sleep(2)
    ans=driver.find_elements(By.XPATH,'//div[@role="none"]')
    for i in ans:
        if i.text.split()[0]==account:
            i.click()
            break
    time.sleep(5)
    details=analysis(finding_comments())
    a=[]
    name=[]
    for i in details:
        name.append(i)
        a.append(details[i])
    df=pd.DataFrame(a)
    fig=px.pie(df, names=name, title='comments sentiment analysis')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("analysis.html",output=details,graphJSON=graphJSON)
def finding_comments():
    post = driver.find_element(By.CLASS_NAME,"_aagu")
    post.click()
    j=0
    temp=[]
    while j!=6:
        comments= BeautifulSoup(driver.page_source)
        handles = comments.find_all(class_="_aacl _aaco _aacu _aacx _aad7 _aade")
        count=0
        for i in handles:
            if count!=5:
                print(i.text)
                temp.append(i.text)
                count+=1
                time.sleep(2)
        next = driver.find_element(By.XPATH,'//div[(@class = " _aaqg _aaqh")]')
        next.click()
        time.sleep(2)
        j+=1
    return temp   
def analysis(temp):
    details = {}
    analyzer=SentimentIntensityAnalyzer()
    for i in temp:
        en=analyzer.polarity_scores(i)
        for j in en:
            if j not in details:
                details[j]=en[j]
            else:
                details[j]+=en[j]
    return details   
app.run( port=5001, debug=True)