from flask import Flask
import mysql
from os import listdir
import os
import time
from os.path import isfile, join
from bs4 import BeautifulSoup
from instabot import Bot
import time
import random
import requests
from flask_mysqldb import MySQL
from flask import  get_flashed_messages, session,Flask,render_template,redirect,request,flash,url_for
app=Flask(__name__)

mydb=MySQL(app)











def insert_domain(domain,list):
    if domain in list:
        print('domain in list')
    else:
        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO DOMAINS(URL)VALUES(%s)',(domain,))
            mydb.connection.commit()
        list.append(domain)

def remove_config():
    try:
        mypath='config'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for files in onlyfiles:
            os.remove(mypath+'/'+files)
        print('files removed for config')

        try:
            pycache='__pycache__'
            onlyfiles = [f for f in listdir(pycache) if isfile(join(pycache, f))]
            for file in onlyfiles:
                os.remove(pycache+'/'+file)
            print('files removed for pycache')
        except:
            print('pycache files not found')

        logfile='config/log'
        onlyfiles = [f for f in listdir(logfile) if isfile(join(logfile, f))]
        for files in onlyfiles:
            os.remove(logfile+'/'+files)
        print('log files removed')

        os.rmdir('config/log')
        os.rmdir(mypath)
        os.rmdir('__pycache__')
        print('success')
    except:
        print('directories not found')
bot=Bot()
def login(username,password):
    try:
        remove_config()
    except:
        pass
    try:
        
        bot.login(username=username,password=password)
    except:
        Alert=('The Bot is not functioning Right now... try again Later')
        print(Alert)


def last_resort():
    #ensure images is like 'images/'
    images='images'
    import random
    captions=('😂😂😂🤣🤣','Kwishaaa💀💀','#kenyasihami','#trendymemes','Trendingmemes')
    caption=random.choice(captions)
    caption=str(caption)+"    We bring you Kenya's finest content... Dont forget to like,share and follow"
    for image in os.listdir(images):
        path=images+'/'+image
        try:
            bot.upload_photo(path,caption='We Bring you the Finest Content Daily😂🔥😋  #memes')
            time.sleep(5)
        except:
            pass
        try:
            os.remove(path)
        except:
            os.remove(str(path)+'.REMOVE_ME')

def resize(path):
    from PIL import Image
    image = Image.open(path)
    image = image.resize((547,609),Image.ANTIALIAS)
    import os
    os.remove(path)
    image.save(fp=path)

'''def post_to_gram(file):
    bot = Bot()
    bot.login(username = "",
          password = "")
    bot.upload_photo(file,caption='#kenyantrendingmemes #kenyantrendingimages ')

    remove_config()'''


def obtain_images(url1):
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM IMAGES WHERE URL="'+url1+'"')
        fff=cursor.fetchall()
        
        try:
            foru=[]
            for ffx in fff:
                for ffx in ffx:
                    foru.append(ffx)
                
            print(foru)
            if url1 in foru:
                print('the url already exists')
            else:
                url=str(url1)
                r = requests.get(url, allow_redirects=True)
                file=random.randint(1,100000)
                file='images/'+str(file)+'.png'
                open(file, 'wb').write(r.content)
                cursor=mydb.connection.cursor()
                cursor.execute('INSERT INTO IMAGES(URL)VALUES(%s)',(url,))
                mydb.connection.commit()
                print('Successfully uploaded to database')
                
        except:
            print('route 2')
            url1=str(url1)
            
            r = requests.get(url1, allow_redirects=True)
            
            file=random.randint(1,100000)
            
            file='images/'+str(file)+'.png'
            
            open(file, 'wb').write(r.content)
            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO IMAGES(URL)VALUES(%s)',(url1,))
            mydb.connection.commit()
            print('Successfully uploaded to database')
            




list_of_domains=[]
def fetch_from_list(list):
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM DOMAINS')
    domains=cursor.fetchall()
    for dormain in domains:
        for minidomain in dormain:
            if minidomain in list:
                pass
            else:
                list.append(minidomain)

def clear_database():
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('DELETE FROM DOMAINS')
        mydb.connection.commit()
        print('database cleared')
        list_of_domains.clear()

def post(url):
    for number in range(1,20):
        x=url.format(number)
        print(1)
        obtain_images(x)
        print(2)
        last_resort()
        print(3)
        time.sleep(5)

url='https://nairobiwire.com/wp-content/uploads/2021/12/trend{}-12.jpg'
@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        

        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT * FROM DOMAINS')
            fff=cursor.fetchall()
        domains=[]
        for x in fff:
            for fln in x:
               domains.append(fln)
        
    
        #if activator is checked
        try:
            if 'activator' in request.form['activator']:
                username=request.form.getlist('usernamex')
                list_of_passwords=[]
                
                for username in username:
                    print(username)
                    with app.app_context():
                        cursor=mydb.connection.cursor()
                        cursor.execute('SELECT PASSWORD FROM INSTANAMES WHERE USERNAME="'+username+'"')
                        fff=cursor.fetchall()
                    for xxl in fff:
                        for password in xxl:
                            list_of_passwords.append(password)
                            print(password)
                            #login and post
                            login(username,password)
                            for domain in domains:
                                post(domain)

                #login(username,password)
                ### Post the Domains
                #for domain in domains:
                    #pass
                    #post(domain)
        except:
            pass
                #take the url
        try:
            url=str(request.form['url'])
            if url in domains:
                print('the domain already exists')
                pass
            elif url=='':
                pass
            elif url==' ':
                pass
            else:
                cursor=mydb.connection.cursor()
                cursor.execute('INSERT INTO DOMAINS(URL)VALUES(%s)',(url,))
                mydb.connection.commit()
                domains.append(url)
                print('added')


        except:
            print('error')

        #get usernames
        usernames=[]
        passwords=[]
        username=str(request.form['username'])
        password=str(request.form['password'])
        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT USERNAME FROM INSTANAMES')
            fff=cursor.fetchall()
        for fln in fff:
            for x in fln:
                usernames.append(x)

        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT PASSWORD FROM INSTANAMES')
            fff=cursor.fetchall()
        for fln in fff:
            for x in fln:
                passwords.append(x)

        if username in usernames:
            pass
        elif username=='':
            pass
        else:
            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO INSTANAMES(USERNAME,PASSWORD)VALUES(%s,%s)',(username,password))
            mydb.connection.commit()
            usernames.append(username)
            passwords.append(password)
        
        #Clear Usernames
        try:
            if 'clear_usernames' in request.form['clear_usernames']:
                usernames.clear()
                cursor=mydb.connection.cursor()
                cursor.execute('DELETE FROM INSTANAMES')
                mydb.connection.commit()
        except:
            pass
        #clear domains
        try:
            if 'clear_domains' in request.form['clear_domains']:
                domains.clear()
                with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('DELETE FROM DOMAINS')
                    mydb.connection.commit()
        except:
            pass
            
        

        return render_template('text.html',domains=domains,usernames=usernames)
    else:
        #load domains
        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT * FROM DOMAINS')
            fff=cursor.fetchall()
        domains=[]
        try:
            for x in fff:
                for fln in x:
                   domains.append(fln)
            
        except:
            pass
        #load usernames
        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT USERNAME FROM INSTANAMES')
            fff=cursor.fetchall()
        usernames=[]
        for x in fff:
            for fln in x:
               usernames.append(fln)
        return render_template('text.html',domains=domains,usernames=usernames)

if __name__=='__main__':
    app.run(debug=True)
