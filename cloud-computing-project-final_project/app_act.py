from flask import Flask, jsonify, request, abort
import requests
import re
import pickle
app = Flask(__name__)
app_count = 0
health_flag = 0
# categories = set(["category1", "category2"]);
#
# no_of_acts_categories_dict = {
#     "category1" : 0,
#     "category2" : 0,
# }
#
#
# range_list = []
k=0
#
# acts_list_categories_dict = {
#     "category1" : [],
#     "category2" : [],
# }
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Origin','35.170.87.49')
  return response

# 3_final [List all categories]
@app.route('/api/v1/categories', methods=['GET'])
def list_categories():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    if(len(categories) > 0):
        return jsonify(no_of_acts_categories_dict),200
    else:
        return jsonify({}),204


# 4_final  [Add a category]
@app.route('/api/v1/categories', methods=['POST'])
def add_category():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    if request.json[0] not in categories:
        category = request.json[0]
        no_of_acts_categories_dict[category] = 0
        acts_list_categories_dict[category] = []
        categories.add(category)
    else:
        abort(405)
    return jsonify({}), 201

# 5_final  [Remove a category]
@app.route('/api/v1/categories/<string:categoryName>', methods=['DELETE'])
def remove_category(categoryName):
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    if categoryName in no_of_acts_categories_dict.keys() and categoryName in categories:
        no_of_acts_categories_dict.pop(categoryName)
        acts_list_categories_dict.pop(categoryName)
        categories.remove(categoryName)
        return jsonify({}), 200
    else:
        abort(405)

# 6_final  [List acts for a given category]
@app.route('/api/v1/categories/<string:categoryName>/acts', methods=['GET'])
def list_acts_for_category(categoryName):
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    if 'start' in request.args and 'end' in request.args:
        startRange = int(request.args.get('start'))
        endRange = int(request.args.get('end'))
        if categoryName not in no_of_acts_categories_dict.keys():
            return jsonify([]), 405
        elif (startRange<1) or (endRange>no_of_acts_categories_dict[categoryName]):
            abort(400)
        elif (endRange-startRange+1>100):
            abort(413)
        else:
            ans = []
            i = len(acts_list_categories_dict[categoryName])-startRange
            f = endRange-startRange+1
            while(f>0):
                ans.append(acts_list_categories_dict[categoryName][i])
                i = i-1
                f = f-1
            return jsonify(ans), 200
    if categoryName in acts_list_categories_dict:
        acts_list = acts_list_categories_dict[categoryName]
        len_acts_list = len(acts_list)
        if(len_acts_list == 0):
            return jsonify([]), 204
        elif(len_acts_list > 100) :
            abort(413)
        else:
            return jsonify(acts_list), 200
    else:
        abort(405)


# 7_final [Number of acts in a category]
@app.route('/api/v1/categories/<string:categoryName>/acts/size', methods=['GET'])
def number_of_acts_for_category(categoryName):
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    if categoryName not in no_of_acts_categories_dict.keys():
        return jsonify([]), 405
    elif categoryName in no_of_acts_categories_dict.keys():
        return jsonify([no_of_acts_categories_dict[categoryName]])
    else:
        abort(405)

# 9_final [Upvote an act]
@app.route('/api/v1/acts/upvote', methods=['POST'])
def upvote_an_act():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    for i in acts_list_categories_dict.values():
        for j in i:
            if j["actId"]==request.json[0]:
                j["upvotes"] = j["upvotes"]+1
                return jsonify({}), 200
    abort(405)
# 10_final [Remove an act]
@app.route('/api/v1/acts/<int:task_id>',methods = ['DELETE'])
def delete_act(task_id):
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    # for i in acts_list_categories_dict.values():
    #     for j in range(len(i)):
    #         if j["actId"]==task_id:
    #             del(j)
    #             return jsonify({}), 200
    category_list = list(acts_list_categories_dict.keys())
    for i in (category_list):
        act_list = acts_list_categories_dict[i]
        flag = 0
        for j in range(len(act_list)):
            if(act_list[j]["actId"] == task_id):
                del(act_list[j])
                no_of_acts_categories_dict[i] = no_of_acts_categories_dict[i] - 1
                return jsonify({}),200
    abort(405)

@app.route('/api/v1/acts', methods=['POST'])
def upload_an_act():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    #The ​actID​ in the request body must be globally unique(1,7)
    for i in acts_list_categories_dict.values():
        for j in i:
            if j["actId"]==request.json["actId"]:
                abort(405)

    #Validatin date and time (2)
    if(not re.match('[0-9][0-9]\-[0-9][0-9]\-[0-9][0-9][0-9][0-9]:[0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]', request.json["timestamp"])):
        abort(400)
    flag = 0
    # assuming the other user container is linked to 0.0.0.0:5000
    req = requests.get("http://54.86.75.218:8000/api/v1/users",headers={"Origin":"35.171.62.224"})
    usernames = req.json()
    for i in usernames:
        if i == request.json["username"]:
            flag = 1
            break
    if flag==0:
        abort(405)


    #No upvotes field should be sent(5)
    if "upvotes" in request.json.keys():
        abort(400)

    #The category name must exist(6)
    if request.json["categoryName"] not in categories:
        abort(405)

    # Validating base_64 password
    # if( not re.match(r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$", json.request["imgB64"])):
    #      abort(400)
    def is_base64(string):
        if len(string) % 4 == 0 and re.match('^[A-Za-z0-9+\/=]+\Z', string):
            return(True)
        else:
            return(False)

    # if (not is_base64(request.json["imgB64"])):
    #     abort(400)

    #Uploading the act
    no_of_acts_categories_dict[request.json["categoryName"]] = no_of_acts_categories_dict[request.json["categoryName"]]+1
    d = dict()
    d["actId"] = request.json["actId"]
    d["timestamp"] = request.json["timestamp"]
    d["caption"] = request.json["caption"]
    d["upvotes"] = 0
    d["imgB64"] = request.json["imgB64"]
    d["username"] = request.json["username"]
    acts_list_categories_dict[request.json["categoryName"]].append(d)
    return jsonify({}), 201

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    pickle.dump(categories, open("categories.p", "wb"))
    pickle.dump(no_of_acts_categories_dict, open("no_of_acts_categories_dict.p", "wb"))
    pickle.dump(range_list, open("range_list.p", "wb"))
    pickle.dump(acts_list_categories_dict, open("acts_list_categories_dict.p", "wb"))
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/api/v1/_count',methods=['GET'])
def count_fun():
    if(health_flag == 1):
        return jsonify({}),500
    count_list = []
    count_list.append(app_count)
    return jsonify(count_list),200

@app.route('/api/v1/_count',methods=['DELETE'])
def del_count():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = 0
    return jsonify({}),200

@app.route('/api/v1/acts/count',methods=['GET'])
def count1():
    if(health_flag == 1):
        return jsonify({}),500
    global app_count
    app_count = app_count + 1
    #if(len(no_of_acts_categories_dict) == 0):
    #    return jsonify({}),405
    count1 = list(no_of_acts_categories_dict.values())
    count_sum = sum(count1)
    l = []
    l.append(count_sum)
    return jsonify(l),200

@app.route('/api/v1/_health',methods=['GET'])
def health_check():
    if(health_flag == 1):
        return jsonify({}),500
    else:
        return jsonify({}),200
@app.route('/api/v1/_crash',methods=['POST'])
def crash_server():
    global health_flag
    health_flag = 1
    return jsonify({}),200
if __name__ == '__main__':
    no_of_acts_categories_dict = pickle.load(open("no_of_acts_categories_dict.p", "rb"))
    categories = pickle.load(open("categories.p", "rb"))
    range_list = pickle.load( open("range_list.p", "rb"))
    acts_list_categories_dict = pickle.load(open("acts_list_categories_dict.p", "rb"))
    app.run("0.0.0.0",port=80)
