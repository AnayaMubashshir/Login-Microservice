from flask import Flask, request, jsonify, redirect, render_template
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URL=os.getenv('MONGO_URL')

client=pymongo.MongoClient(MONGO_URL)
db=client.test
collection=db['FLASK PROJECT']

app=Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    """
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    return 'Hello,  '+name+'! Logged in email id is:'+email
    """
    form_data=dict(request.json)
    collection.insert_one(form_data)
    print(form_data)
    return 'Data submitted from backend'
    
@app.route('/view')
def view():
    data=collection.find()
    data=list(data)
    for item in data:
        print(item)
        del item['_id']
    data={
        'data':data
    }
    return jsonify(data)
    

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9000,debug=True)
