from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import re
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ROG/Desktop/CC/Flask/api_example/backnew.db'

db = SQLAlchemy(app)

#pattern=re.compile([0-9a-z]{40})

def get_time():

    now=str(datetime.datetime.now())
    str1=now[0:-7]
    d=str1[8:10]
    mo=str1[5:7]
    y=str1[0:4]
    h=str1[11:13]
    m=str1[14:16]
    s=str1[17:19]
    timestamp=d+'-'+mo+'-'+y+':'+s+'-'+m+'-'+h
    return timestamp

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Category(db.Model):
    catid=db.Column(db.Integer, primary_key=True)
#    category_id=db.Column(db.String(50),unique=True)
    category_name=db.Column(db.String(50),unique=True)
    #public_id=db.Column(db.String(50),ForeignKey(User.public_id))
    #public_id=db.Column(db.String(50))
    count=db.Column(db.Integer)


class Act(db.Model):
    actid = db.Column(db.Integer,primary_key=True)
#    act_id = db.Column(db.String(50),unique=True)
#    act_name = db.Column(db.String(50))
    #category_id = db.Column(db.Integer,ForeignKey(Category.category_id))
    #public_id = db.Column(db.Integer, ForeignKey(User.public_id))
#    category_id = db.Column(db.String(50))
    username=db.Column(db.String(50))
    catid=db.Column(db.Integer)
    caption = db.Column(db.String(100))
    #public_id = db.Column(db.String(50))
    image = db.Column(db.String(100))
    timestamp = db.Column(db.String(20))
    upvotes = db.Column(db.Integer)

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
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

'''

@app.route('/api/v1/users', methods=['GET'])
#@token_required
def get_all_users():

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
        return jsonify({"message":"No users in the database"}),204
    #users = User.query.limit(2)

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
#        user_data['public_id'] = user.public_id
        user_data['username'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output}),200



@app.route('/api/v1/users', methods=['POST'])
#@token_required
def create_user():
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    data = request.get_json()

    if User.query.filter_by(name=data['username']).count()>0:
        return jsonify({"message":"The username has already been taken"}),500

#    isValidSHA1(data['password'])
    #pattern=re.compile([0-9a-z]{40})
    password=lower(data['password'])
    x=re.search("[a-z0-9]",password)
    if not (x):
        return jsonify({"message":"the password is not in the method specified"}),400
#    hashed_password = generate_password_hash(data['password'], method='sha1')

    new_user = User(name=data['username'], password=password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'}),201



@app.route('/api/v1/users/<username>',methods=['DELETE'])

def delete_user(username):
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''

    users=User.query.filter_by(name=username).first()

    if not users:
        return jsonify({'message':'The user id is invalid'}),400

    db.session.delete(users)
    db.session.commit()

    return jsonify({'message':'The user has been deleted'}),200

@app.route('/api/v1/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        #token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        #return jsonify({'token' : token.decode('UTF-8')})
        if user.admin:
            return jsonify({"message":"admin privileges authorized, login successful"})
        return jsonify({"message":"login successful!"})


    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/api/v1/users/<username>', methods=['PUT'])
#@token_required
def promote_user( username):
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    user = User.query.filter_by(name=username).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})




@app.route('/api/v1/categories',methods=['GET'])
#@token_required
#def get_all_categories(current_user):

def get_all_categories():
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    #    return jsonify({"message":"its working"})
    Categories=Category.query.all()
    '''
    Category.query.filter_by(category_name=data['categoryName']).update().values(count=Act.query.filter_by(catid=Categories.catid).count())
    '''
    if Category.query.count()==0:
        return jsonify({'message': 'no categories to display'}),204



    output=[]
    for category in Categories:
        category_data = {}
        category_data['category_id']=category.catid
        category_data['categoryName']=category.category_name
        category_data['count']=category.count
 #        category_data['public_id']=category.public_id
        output.append(category_data)

#    output.headers.add('Access-Control-Allow-Origin', '*')

    return jsonify({'categories' : output}),200



@app.route('/api/v1/categories/<category_name>/acts', methods=['GET'])

def get_all_acts_in_category(category_name):

    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''

    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({'message' : 'No such category found!'}),400


    Categories=Category.query.filter_by(category_name=category_name).first()
    #return jsonify({'cat_id':str(Categories.category_id)})


    Acts=Act.query.filter_by(catid=Categories.catid)

    if Acts.count()==0:
        return jsonify({"message":"no acts in this category"}),204

    if Acts.count()>100:
        return jsonify({"message":"No of acts greater than 100"}),413

    #rows=Categories.query

    output=[]
    for act in Acts:
        #if Act.category==
        act_data = {}
        act_data['actId'] = act.actid
        act_data['username'] = act.username
#        act_data['act_id'] = act.act_id
#        act_data['act_name'] = act.act_name
        act_data['caption'] = act.caption
        act_data['imgB64'] = act.image
        act_data['catid'] = act.catid
        act_data['categoryName'] = Categories.category_name
#        act_data['public_id'] = act.public_id
        act_data['timestamp'] = act.timestamp
        output.append(act_data)

    return jsonify({'acts_in_category' : output}),200



@app.route('/api/v1/categories',methods=['POST'])

def upload_category():
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    #Categories=Act.query.all()
    data = request.get_json()
    if Category.query.filter_by(category_name=data['categoryName']).count()>0:
        return jsonify({"message":"Category with that name already exists"}),400
#    new_category = Category(category_id=)
    new_category = Category( category_name=data['categoryName'],count=0 )

    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message' : 'New category added!'}),201

@app.route('/api/v1/acts',methods=['POST'])

def upload_act():
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    flag=0
    data=request.get_json()

    users=User.query.filter_by(name=data['username']).first()

    if User.query.filter_by(name=data['username']).count()==0:
        return jsonify({"message":"no such user found!"}),400

    Categories=Category.query.filter_by(category_name=data['categoryName']).first()

    if Category.query.filter_by(category_name=data['categoryName']).count()==0:
        return jsonify({'message' : 'No such category found!'}),400

    if Act.query.filter_by(actid=data['actId']).count()>0:
        return jsonify({"message":"actId entered is already taken"}),400

    if not re.search("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$",data['imgB64']):
        return jsonify({"message":"Image not in B64 encoding"}),400

    if data['timestamp'][2]=='-' and data['timestamp'][5]=='-' and data['timestamp'][10]==':' and data['timestamp'][13]=='-' and data['timestamp'][16]=='-' and len(re.findall("[0-9]",data['timestamp']))==14:
        flag =1
    if flag!=1:
        return jsonify({"message":"The timestamp is not in proper format"}),400



#    return jsonify({'cat_id':str(Categories.category_id)})

#    queried_category_id=Categories.category_id
#    return jsonify({'time':str(get_time())})
#    new_act = Act(username=data['username'],actid=data['actId'], catid=Categories.catid,caption=data['caption'],  image=data['imgB64'],timestamp=str(get_time()) ,upvotes=0)
    new_act = Act(username=data['username'],actid=data['actId'], catid=Categories.catid,caption=data['caption'],  image=data['imgB64'],timestamp=data['timestamp'] ,upvotes=0)

#    Categories.update().values(count=count+1)
    db.session.add(new_act)
    db.session.commit()
#    Category.query.filter_by(category_name=data['categoryName']).update(Category).values(count=Act.query.filter_by(catid=Categories.catid).count())
#    counts=Category.query.filter_by(category_name=data['categoryName']).count#=Category.query.filter_by(category_name=data['categoryName']).count+1
#    counts=counts+1
#    Category.query.filter_by(category_name=data['categoryName']).count=counts
    db.session.commit()

    return jsonify({'message' : 'new act uploaded'}),201
'''
@app.route('/acts',methods=['PUT'])

def increment_count():
    data.request.get_json()

    Categories=Category.query.filter_by(category_name=data['categoryName']).first()
    if Category.query.filter_by(category_name=data['categoryName']).count()==0:
        return jsonify({'message' : 'No such category found!'})






'''

@app.route('/api/v1/acts/<act_id>', methods=['DELETE'])

#def delete_act(category_name,public_id,act_name):
def delete_act(act_id):
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    ''''''
    user=User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    '''
    act=Act.query.filter_by(actid=act_id).first()
    if act.count()==0:
        return jsonify({'message': 'No such act found'}),400

    db.session.delete(act)
    db.session.commit()

    return jsonify({'message':'The act has been deleted'}),200

@app.route('/api/v1/categories/<category_name>',methods=['DELETE'])
#@app.route('/category/<category_id>',methods=['DELETE'])

def delete_category(category_name):
#def delete_category(category_id,public_id):
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    #return jsonify({"category_id":category_id})

    #user=User.query.filter_by(public_id=public_id)
    '''
    if not user:
        return jsonify({'message' : 'No user found!'})
    '''
    categories=Category.query.filter_by(category_name=category_name).first()
    #return jsonify({"cat id":str(categories.category_id)})

    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({"message":"no such category exists"}), 400

    acts=Act.query.filter_by(catid=categories.catid).count()

    if acts!=0:
        return jsonify({'message' : 'The category has acts in it, delete them first and then delete the category'}),403
    '''
    if categories.public_id!=public_id:
        return jsonify({'message':'unauthorized'})
    '''
    db.session.delete(categories)
    db.session.commit()

    return jsonify({'message' : 'The category has been deleted'}),200

#@app.route('/categories/<category_name>/acts?start=<int:start_range>&end=<int:end_range>',methods=['GET'])
@app.route('/api/v1/categorie/<category_name>/acts',methods=['GET'])
#@app.route('/api/v1/categories/<category_name>/acts?start=<start_range>&end=<end_range>',methods=['GET'])

def get_acts_in_range(category_name):
    start_range=int(request.args.get('start'))
    end_range=int(request.args.get('end'))
#    start_range=int(start_range)
#    end_range=int(end_range)

    #return jsonify({"start":str(start_range),"end":str(end_range)})
    categories=Category.query.filter_by(category_name=category_name).first()
    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({"message":"category name not found!"}),400

    acts=Act.query.filter_by(catid=categories.catid)

    if Act.query.filter_by(catid=categories.catid).count()>100:
        return jsonify({"message":"no of acts morethan 100"}),413

    if Act.query.filter_by(catid=categories.catid).count()==0:
        return jsonify({"message":"no of acts found"}),204


    output=[]
    for act in acts:
        if act.actid>=start_range and act.actid<=end_range:
            act_data={}
            act_data['actId'] = act.actid
            act_data['username'] = act.username
    #        act_data['act_id'] = act.act_id
    #        act_data['act_name'] = act.act_name
            act_data['caption'] = act.caption
            act_data['imgB64'] = act.image
            act_data['catid'] = act.catid
            act_data['categoryName'] = categories.category_name
    #        act_data['public_id'] = act.public_id
            act_data['timestamp'] = act.timestamp
            output.append(act_data)

    return jsonify({"acts":output}),200

@app.route('/api/v1/acts/upvote',methods=['POST'])

def upvote():
    data=request.get_json()
    acts=Act.query.filter_by(actid=data['actId']).first()
    if acts.count()==0:
        return jsonify({"message":"act not found"}),400
#    act.update().values(upvotes=upvotes+1)
    db.session.add(new_act)
    db.session.commit()

    return jsonify({"message":"upvote successful"}),200


@app.route('/api/v1/categories/<category_name>/acts/size',methods=['GET'])

def get_size_of_category(category_name):

    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({'message' : 'No such category found!'}),400


    Categories=Category.query.filter_by(category_name=category_name).first()
    #return jsonify({'cat_id':str(Categories.category_id)})


    Acts=Act.query.filter_by(catid=Categories.catid)

    return jsonify({"message":str(Acts.count())}),200

    '''
    if Acts.count()==0:
        return jsonify({"message":"no acts in this category"}),204

    if Acts.count()>100:
        return jsonify({"message":"No of acts greater than 100"}),413

    #rows=Categories.query

    output=[]
    for act in Acts:
        #if Act.category==
        act_data = {}
        act_data['actId'] = act.actid
        act_data['username'] = act.username
#        act_data['act_id'] = act.act_id
#        act_data['act_name'] = act.act_name
        act_data['caption'] = act.caption
        act_data['imgB64'] = act.image
        act_data['catid'] = act.catid
        act_data['categoryName'] = Categories.category_name
#        act_data['public_id'] = act.public_id
        act_data['timestamp'] = act.timestamp
        output.append(act_data)

    return jsonify({'acts in category' : output}),200

    '''



if __name__=='__main__':
    app.run(debug=True)
