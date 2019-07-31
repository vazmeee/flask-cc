from flask import Flask, request, jsonify, make_response, render_template
#from flask_sqlalchemy import SQLAlchemy
#import uuid
#from werkzeug.security import generate_password_hash, check_password_hash
#import jwt
#import datetime
#from functools import wraps
#import re
from flask_cors import CORS, cross_origin
import requests
#import base64
import json

app = Flask(__name__)
CORS(app)

#app.config['SECRET_KEY'] = 'thisissecret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ROG/Desktop/CC/Flask/api_example/backnew.db'

#db = SQLAlchemy(app)

@app.route('/front',methods=['GET'])
def print_something():
    r=requests.get("http://127.0.0.1:5000/api/v1/categories/category2/acts").json()
    #return jsonify({"frontendmessage":r})
    return json.dumps(r)
    #resp=requests.post(url='http://127.0.0.1:5001/front')
    #return render_template('')
    #return jsonify({"from frontend":resp})

@app.route('/front/post',methods=['POST'])
def post_something():
    x={"username":"theonefromfrontend","password":"649de402fcc1cda241a2a48a90c68754ec2196b5"}
    resp=requests.post('http://127.0.0.1:5000/api/v1/users',x)
    return json.dumps(resp.json())


if __name__=='__main__':
    app.run(debug=True,port=5001)
