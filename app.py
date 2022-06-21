from auth import *
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from bson.json_util import dumps
import datetime as dt 
import csv
import json
import os


app = create_app()

#connect to MongoDB
import pymongo
connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['ECA']
records = db.useraccount
catalogrecords = db.catalogrecords
import json

@app.route('/', methods=['POST','GET'])
def main():
    if request.method =="GET":
        return render_template('index.html')
    elif request.method == "POST":
        email = request.form.get('Loginemail')
        password = request.form.get('Loginpsw')
        user = UserAccount.get_user_byEmail(email=email)

        if not user or not check_password_hash(user._data['password'], password):
            message = "*please check your login details and try again"
            return render_template('index.html', message=message)
    
        login_user(user)
        session["email"] = email 
        return render_template('catalog.html', email=email)

@app.route('/index', methods=['POST','GET'])
def index():

    # if request.method =="GET":
    #     return render_template('index.html')
    if request.method == "POST":
        email = request.form.get('Loginemail')
        password = request.form.get('Loginpsw')
        user = UserAccount.get_user_byEmail(email=email)
        if not user or not check_password_hash(user._data['password'], password):
            message = "*please check your login details and try again"
            return render_template('index.html', message=message)
    
        login_user(user)
        session["email"] = email    
        return redirect(url_for('catalog',email=email))
    return render_template('index.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "email" in session:
        session.pop("email", None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')

    elif request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("psw")
        nric = request.form.get("enNRIC")

        user = UserAccount.get_user_byEmail(email=email)

        if user:
            message = ('*Email address already exist')
            return render_template('register.html', message=message)
           

        new_user = UserAccount(email=email,password=generate_password_hash(password, method='sha256'), nric=nric)
    return redirect(url_for('index'))


@app.route('/catalog' , methods=['POST','GET'])
def catalog():
    twrecord = 0

    if "email" in session:
        email = session["email"]

        if request.method =="POST":
            whend = request.form['when']
            year, month, day = whend.split('-')
            session["year"] = year
            whenl = '-'.join([year, month, day]) + ' 00:00:00'
            when = dt.datetime.fromisoformat(whenl)
            who = request.form['who']
            comment = request.form['comment']
            about = request.form['about']
            media = request.form['media']
            what = request.form['what']
            whom = request.form['whom']
            refid = request.form['refid']
            catalog_input ={'when' : when, 'who': who, 'comment' : comment,'about': about, "media" : media, "what" : what, "whom" : whom, "refid" : refid}
            catalogrecords.insert_one(catalog_input)
            
        return render_template("catalog.html", email=email)

    else:
        if request.method =="POST":
            whend = request.form['when']
            year, month, day = whend.split('-')
            session["year"] = year
            whenl = '-'.join([year, month, day]) + ' 00:00:00'
            when = dt.datetime.fromisoformat(whenl)
            who = request.form['who']
            comment = request.form['comment']
            about = request.form['about']
            media = request.form['media']
            what = request.form['what']
            whom = request.form['whom']
            refid = request.form['refid']
            catalog_input ={'when' : when, 'who': who, 'comment' : comment,'about': about, "media" : media, "what" : what, "whom" : whom, "refid" : refid}
            catalogrecords.insert_one(catalog_input)
            
      



    return render_template('catalog.html')

@app.route('/getyearsrange', methods=['POST','GET'])
def getyears():
    yearsrange = catalogrecords.aggregate([
         {
                "$match" : {"who" : "@suss_sg"}
         },
         {
                "$group" : {
                    "_id" : {
                        "year" : {"$year" : "$when"}
                    },
                "count" :{"$sum" :1}
                }
         
            },
                {
                "$sort" : {"_id.year" : -1}
                }

        ])
    years = dumps(yearsrange)
    years2 = json.loads(years)
    li = [item.get('_id') for item in years2]
    li2 = [item.get('year') for item in li]
    li3 = [item.get('count') for item in years2]
    dict_data = {}
    for key in li2:
        for value in li3:
            dict_data[key] = value
            li3.remove(value)
            break
    for key,value in dict(dict_data).items():
        if value < 12:
            dict_data.pop(key)
    listofyear = [k for k in dict_data]
    return jsonify({'yearsrange':json.dumps(listofyear)})

 

@app.route('/getdashboardpermonth', methods=['POST','GET'])
def databypermonth():
    #get request from ajax selected year
    Syear = request.get_json(force=True)
    Syear1 = json.dumps(Syear)
    Syear2 = json.loads(Syear1)['year']
    
    #check condition from ajax select year is not "all"
    if Syear2 != "all":
        SyearStart = str(Syear2) + "-01-01 00:00:00.000Z"
        SyearEnd = str(Syear2) + "-12-31 23:59:59.000Z"
        SyearStartDT = dt.datetime.strptime(SyearStart, "%Y-%m-%d %H:%M:%S.%fZ" )
        SyearEndDT = dt.datetime.strptime(SyearEnd,  "%Y-%m-%d %H:%M:%S.%fZ" )

        Trendbymonth = catalogrecords.aggregate([
            {
                "$match" : {"who" : "@suss_sg"}

            },
            
            {
                "$match" : {
                    "when" :
                    {
                        "$gte" : SyearStartDT,
                        "$lt" : SyearEndDT

                    }
                }

            },
            {
                "$group" : {
                    "_id" : {
                        "month" : {"$month" : "$when"}
                    },
                "count" :{"$sum" :1}

                }

            },
                
                {
                "$sort" : {"_id.month" : 1}
                }
                

        ]
        
        )
        twitter_data = dumps(Trendbymonth)
        twitter_data2 = json.loads(twitter_data)
        li = [item.get('_id') for item in twitter_data2]
        li2 = [item.get('month') for item in li]
        li3 = [item.get('count') for item in twitter_data2]

        # create raw data to match missing
        rawdictionary = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

        dict_data = {}
        for key in li2:
            for value in li3:
                dict_data[key] = value
                li3.remove(value)
                break

        # match data for rawdictionary and the dict_data
        for key,value in rawdictionary.items():
            if(key in dict_data and rawdictionary):
               pass
            else :
                dict_data[key] = value
                
        #sort it back 
        sorted_dict_data = dict(sorted(dict_data.items()))
        labels = list(sorted_dict_data.keys())
        data = list(sorted_dict_data.values())

        return jsonify({'tweets':json.dumps({'data':data,'labels':labels})})
    return ''
@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    if "email" in session:
        email = session["email"]
        return render_template('dashboard.html', email=email)


    return render_template('dashboard.html' )
@app.route('/data' , methods=['POST','GET'])
def data():
    twitterTrend = catalogrecords.aggregate([
            {
                "$match" : {"who" : "@suss_sg"}
            },
            {
                "$group" : {
                    "_id" : {
                        "year" : {"$year" : "$when"}
                    },
                "count" :{"$sum" :1}

                }
                

            },
               
                {
                "$sort" : {"_id.year" : 1}
                }
               

        ]
       
        )

    twitter_data = dumps(twitterTrend)
    twitter_data2 = json.loads(twitter_data)
    li = [item.get('_id') for item in twitter_data2]
    li2 = [item.get('year') for item in li]
    li3 = [item.get('count') for item in twitter_data2]

    dict_data = {}
    for key in li2:
        for value in li3:
            dict_data[key] = value
            li3.remove(value)
            break
    labels = list(dict_data.keys())
    data = list(dict_data.values())

    return jsonify({'tweets':json.dumps({'data':data,'labels':labels})})

@app.route('/upload', methods=['POST','GET'])
def upload():
    if "email" in session:
        Ijarray = []
        email = session["email"]
        if request.method=="POST" :
            f = request.form['fileupload']
            
            message = "Upload Completed!"
            with open(f, encoding='utf-8') as csvfile: 
                csvR = csv.DictReader(csvfile)
                for row in csvR:
                    row['when'] = dt.datetime.strptime(row['when'], "%m/%d/%Y")
                    row['when'].replace(microsecond=0)
                    Ijarray.append(row)
               
                
                catalogrecords.insert(Ijarray)

            return render_template("upload.html", email=email, message=message)

    return render_template('upload.html', email=email)



if __name__ == "__main__":
    app.run(debug=True)