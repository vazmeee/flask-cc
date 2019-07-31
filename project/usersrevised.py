from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import re
import json
#from flask_jwt import JWT
from sys import getsizeof


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///backnew.db"

db = SQLAlchemy(app)

api_count=0
api_count_fail=0
api_count_success=0


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

'''
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(name=data['name']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
'''


@app.route('/api/v1/users', methods=['GET'])
#@token_required
def get_all_users():
    global api_count
    global api_count_success
    global api_count_fail

    '''
    if request.method !='GET':
        return jsonify({"message":"Invalid method"}),405
    '''

    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    users = User.query.all()
    if User.query.count()==0:



        api_count+=1
        api_count_fail+=1

        return jsonify({"message":"No users in the database"}),204
    #users = User.query.limit(2)

#    output = []
    x=[]
    for user in users:
        user_data = {}
#        user_data['id'] = user.id
#        user_data['public_id'] = user.public_id
#        user_data['username'] = user.name
#        user_data['password'] = user.password
#        user_data['admin'] = user.admin
#        output.append(user_data)
        x.append(user.name)

    api_count+=1
    api_count_success+=1

#    return jsonify({'users' : output}),200
    return jsonify(x),200


@app.route('/api/v1/users', methods=['POST'])
#@token_required
def create_user():
    global api_count
    global api_count_success
    global api_count_fail
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    data = request.get_json()

    if User.query.filter_by(name=data['username']).count()>0:



        api_count+=1
        api_count_fail+=1

        return jsonify({"message":"The username has already been taken"}),400

#    isValidSHA1(data['password'])
    #pattern=re.compile([0-9a-z]{40})
    password=data['password']
    password=password.lower()
#    password=lower(data['password'])
    x=re.search("[a-z0-9]",password)
#    if not (x):
#        return jsonify({"message":"the password is not in the method specified"}),400
    hashed_password = generate_password_hash(data['password'], method='sha1')
#    hashed_password=hashed_password[:40]
#    return jsonify({"pass",str(getsizeof(str(hashed_password)))})
    #jsonify({'pass':hashed_password})
    new_user = User(name=data['username'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()


    api_count+=1
    api_count_success+=1

    return jsonify({'message' : 'New user created!'}),201



@app.route('/api/v1/users/<username>',methods=['DELETE'])
#@token_required
def delete_user(username):
    global api_count
    global api_count_success
    global api_count_fail
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''

    users=User.query.filter_by(name=username).first()

    if not users:



        api_count+=1
        api_count_fail+=1

        return jsonify({'message':'The user id is invalid'}),400

    db.session.delete(users)
    db.session.commit()


    api_count+=1
    api_count_success+=1

    return jsonify({'message':'The user has been deleted'}),200

@app.route('/api/v1/login')
def login():
    global api_count
    global api_count_success
    global api_count_fail
    auth = request.authorization

    if not auth or not auth.username or not auth.password:



        api_count+=1
        api_count_fail+=1

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:



        api_count+=1
        api_count_fail+=1

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    '''
#    if check_password_hash(user.password, auth.password):
    if user.password==auth.password:
        jjwt=jwt.JWT()
        tok={'username' : user.name, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30) }
        #tok2=json.dumps(tok)
#        token = jjwt.encode({'username' : user.name, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30) }, app.config['SECRET_KEY'])
        token = jjwt.encode(str(tok),app.config['SECRET_KEY'])
    '''
    if user.password==auth.password:
        token=jwt.encode({'name':user.name,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
        if user.admin:


            api_count+=1
            api_count_success+=1

            return jsonify({"message":"admin privileges authorized, login successful"})


        api_count+=1
        api_count_success+=1

        return jsonify({"message":"login successful!"})



    api_count+=1
    api_count_fail+=1


    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



@app.route('/api/v1/users/<username>', methods=['PUT'])
#@token_required
def promote_user( username):
    global api_count
    global api_count_success
    global api_count_fail
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    user = User.query.filter_by(name=username).first()

    if not user:



        api_count+=1
        api_count_fail+=1

        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()


    api_count+=1
    api_count_success+=1

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/api/v1/_count',methods=['GET'])
def get_api_count():
    return jsonify([str(api_count)])
    return jsonify({'count':{'total':str(api_count),'successful':str(api_count_success),'failed':str(api_count_fail)}}),200

@app.route('/api/v1/_count',methods=['DELETE'])
def reset_count():

    global api_count
    global api_count_success
    global api_count_fail
    api_count=0
    api_count_fail=0
    api_count_success=0
    return jsonify({"message":"reset successful"}),200




@app.route('/api/v1/_count',methods=['POST','PUT','PATCH','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def error_count():
    global api_count
    global api_count_success
    global api_count_fail
    methods=['POST','PUT','PATCH','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW']
    for i in methods:
        if request.method==i:
            return jsonify({"message":"method not allowed"}),405



@app.route('/api/v1/users',methods=['PUT','PATCH','DELETE','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def error1():
    global api_count
    global api_count_success
    global api_count_fail
    methods=['PUT','PATCH','DELETE','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW']



    api_count+=1
    api_count_fail+=1

    for i in methods:
        if request.method==i:
            return jsonify({'message':'method not allowed'}),405


@app.route('/api/v1/users/<username>',methods=['POST','GET','PATCH','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def error2():
    global api_count
    global api_count_success
    global api_count_fail
    methods=['POST','GET','PATCH','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW']



    api_count+=1
    api_count_fail+=1

    for i in methods:
        if request.method==i:
            return jsonify({'message':'method not allowed'}),405




if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
