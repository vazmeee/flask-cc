from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ROG/Desktop/CC/Flask/api_example/back.db'

db = SQLAlchemy(app)


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
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Category(db.Model):
    category_id=db.Column(db.String(50), primary_key=True)
    category_name=db.Column(db.String(50))
    #public_id=db.Column(db.String(50),ForeignKey(User.public_id))
    public_id=db.Column(db.String(50))


class Act(db.Model):
    act_id = db.Column(db.String(50), primary_key=True)
    act_name = db.Column(db.String(50))
    #category_id = db.Column(db.Integer,ForeignKey(Category.category_id))
    #public_id = db.Column(db.Integer, ForeignKey(User.public_id))
    category_id = db.Column(db.String(50))
    public_id = db.Column(db.String(50))
    image = db.Column(db.String(100))
    timestamp = db.Column(db.String(20))



@app.route('/user', methods=['GET'])
#@token_required
def get_all_users():
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/user', methods=['POST'])
#@token_required
def create_user():
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})



@app.route('/user/<id>',methods=['DELETE'])

def delete_user(id):
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''

    users=User.query.filter_by(id=id).first()

    if not users:
        return jsonify({'message':'The user id is invalid'})

    db.session.delete(users)
    db.session.commit()

    return jsonify({'message':'The user has been deleted'})


@app.route('/login')
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
        return jsonify({"message":"login successful!"})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/user/<public_id>', methods=['PUT'])
#@token_required
def promote_user( public_id):
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})




@app.route('/category',methods=['GET'])
#@token_required
#def get_all_categories(current_user):

def get_all_categories():
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    '''
    Categories=Category.query.all()

    if not Categories:
        return jsonify({'message': 'no categories to display'})

    output=[]
    for category in Categories:
        category_data = {}
        category_data['category_id']=category.category_id
        category_data['category_name']=category.category_name
        category_data['public_id']=category.public_id
        output.append(category_data)


    return jsonify({'categories' : output})



@app.route('/category/<category_name>', methods=['GET'])

def get_all_acts_in_category(category_name):

    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''

    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({'message' : 'No such category found!'})


    Categories=Category.query.filter_by(category_name=category_name).first()
    #return jsonify({'cat_id':str(Categories.category_id)})


    Acts=Act.query.filter_by(category_id=Categories.category_id)

    #rows=Categories.query

    output=[]
    for act in Acts:
        #if Act.category==
        act_data = {}
        act_data['act_id'] = act.act_id
        act_data['act_name'] = act.act_name
        act_data['image'] = act.image
        act_data['public_id'] = act.public_id
        act_data['timestamp'] = act.timestamp
        output.append(act_data)

    return jsonify({'acts in category' : output})

@app.route('/category',methods=['POST'])

def upload_category():
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    #Categories=Act.query.all()
    data = request.get_json()
#    new_category = Category(category_id=)
    new_category = Category(category_id=str(uuid.uuid4()), category_name=data['category_name'] , public_id=data['public_id'])

    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message' : 'New category added!'})

@app.route('/category/<category_name>/<public_id>',methods=['POST'])

def upload_act(category_name,public_id):
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    data=request.get_json()



    Categories=Category.query.filter_by(category_name=category_name).first()
    if Category.query.filter_by(category_name=category_name).count()==0:
        return jsonify({'message' : 'No such category found!'})

#    return jsonify({'cat_id':str(Categories.category_id)})

#    queried_category_id=Categories.category_id
#    return jsonify({'time':str(get_time())})
    new_act = Act(act_id=str(uuid.uuid4()),act_name=data['act_name'], public_id=public_id ,category_id=Categories.category_id,  image=data['image'],timestamp=str(get_time()))

    db.session.add(new_act)
    db.session.commit()

    return jsonify({'message' : 'new act uploaded'})


@app.route('/category/<category_name>/<act_id>/<public_id>', methods=['DELETE'])

#def delete_act(category_name,public_id,act_name):
def delete_act(public_id,act_id,category_name):
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    user=User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    act=Act.query.filter_by(act_id=act_id).first()
    if not act:
        return jsonify({'message': 'No such act found'})

    db.session.delete(act)
    db.session.commit()

    return jsonify({'message':'The act has been deleted'})

@app.route('/category/<category_name>/<public_id>',methods=['DELETE'])
#@app.route('/category/<category_id>',methods=['DELETE'])

def delete_category(category_name,public_id):
#def delete_category(category_id,public_id):
    '''
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    '''
    #return jsonify({"category_id":category_id})

    user=User.query.filter_by(public_id=public_id)

    if not user:
        return jsonify({'message' : 'No user found!'})

    categories=Category.query.filter_by(category_name=category_name).first()
    #return jsonify({"cat id":str(categories.category_id)})

    acts=Act.query.filter_by(category_id=categories.category_id).count()

    if acts!=0:
        return jsonify({'message' : 'The category has acts in it, delete them first and then delete the category'})

    if categories.public_id!=public_id:
        return jsonify({'message':'unauthorized'})

    db.session.delete(categories)
    db.session.commit()

    return jsonify({'message' : 'The category has been deleted'})


if __name__=='__main__':
    app.run(debug=True)
