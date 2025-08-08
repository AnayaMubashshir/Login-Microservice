from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests

BACKEND_URL='http://0.0.0.0:9000'
app=Flask(__name__)
@app.route('/')
def home():
    # Get the full name of the current day of the week
    current_day_name = datetime.today().strftime('%A')
    current_time=datetime.now().strftime('%H:%M:%S')
    print(current_day_name)
    return render_template('index.html',day_of_week=current_day_name,current_time=current_time)

@app.route('/submit', methods=['POST'])
def submit():
    current_day_name = datetime.today().strftime('%A')
    current_time=datetime.now().strftime('%H:%M:%S')
    form_data=dict(request.form)
    if not request.form.get('name') or not request.form.get('email') or not request.form.get('password'):
        return render_template('index.html',day_of_week=current_day_name,current_time=current_time,error="All fields are required")
    try:
        response= requests.post(BACKEND_URL+'/submit',json=form_data)
        if response.status_code==200:
            return redirect("/success")
        else:
            return render_template('index.html',error=response.json().get("message","Unknown error"))
    except requests.exceptions.RequestException as e:
        return render_template('index.html',day_of_week=current_day_name,current_time=current_time,error=f"Backend unreachable: {str(e)}")
    

@app.route('/success')
def success():
    return "<h1>Data submitted successfully!<h1>"

@app.route('/get_data')
def get_data():
    response=requests.get(BACKEND_URL+'/view')
    data=response.json()
    data['hello']='world'
    return data

@app.route('/api')
def dataApi():
    response=requests.get(BACKEND_URL+'/view')
    data=response.json()
    return data
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)