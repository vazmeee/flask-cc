
from flask import Flask, jsonify, request, abort,redirect, url_for , Response
import requests
import os
import re
import threading
import sys
import time
dict_container = {}
number_of_req = 0
first_req = 0
no_of_locked_req = threading.Lock()
dict_container_lock = threading.Lock()
app = Flask(__name__)
cur_cont = 0
def auto_scale():
    global number_of_req
    print('Hello world!', file=sys.stderr)
    while(1):
        time.sleep(120)
        no_of_locked_req.acquire()
        dict_container_lock.acquire()
        num_cont_needed = (number_of_req // 20) + 1
        if(len(dict_container) != num_cont_needed):
            if(len(dict_container) < num_cont_needed):
                max_cont_id = max(list(dict_container.keys()))
                extra_cont = num_cont_needed - len(dict_container)
                for i in range(extra_cont):
                    #print("sexxxxx")
                    con = os.popen("docker run -p " + str(max_cont_id + i + 1) + ":80 -d -ti -v database:/db acts6").read()
                    con_real = con.rstrip()
                    dict_container[max_cont_id + i + 1] = con_real
                print(dict_container,file=sys.stderr)
            else:
                #printf("check22")
                max_cont_id = max(list(dict_container.keys()))
                extra_cont = abs(num_cont_needed - len(dict_container))
                while(extra_cont != 0):
                    cont_id_kill = dict_container[max_cont_id]
                    tmp = os.popen("docker container kill " + cont_id_kill).read()
                    del(dict_container[max_cont_id])
                    max_cont_id = max_cont_id - 1
                    extra_cont = extra_cont - 1
                print(dict_container,file=sys.stderr)
        else:
            print("Same number of containers",file=sys.stderr)
        number_of_req = 0
        dict_container_lock.release()
        no_of_locked_req.release()
def init_container():
    print("init")
    con = os.popen("docker run -p 8000:80 -d -ti -v database:/db acts6").read()
    con_real = con.rstrip()
    dict_container[8000] = con_real
#app = Flask(__name__)
@app.route('/api/v1/categories', methods=['GET'])
def fun():
    no_of_locked_req.acquire()
    global first_req
    global number_of_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    #lock for dict_container
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/categories', methods=['POST'])
def cat_post():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/categories/<string:categoryName>', methods=['DELETE'])
def rem_cat(categoryName):
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/categories/<string:categoryName>/acts', methods=['GET'])
def list_acts_for_category(categoryName):
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/categories/<string:categoryName>/acts/size', methods=['GET'])
def number_of_acts_for_category(categoryName):
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/acts/upvote', methods=['POST'])
def upvote_an_act():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/acts/<int:task_id>',methods = ['DELETE'])
def delete_act(task_id):
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/acts', methods=['POST'])
def upload_an_act():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/_count',methods=['GET'])
def count_fun():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/_count',methods=['DELETE'])
def del_count():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

@app.route('/api/v1/acts/count',methods=['GET'])
def count1():
    no_of_locked_req.acquire()
    global number_of_req
    global first_req
    if(first_req == 0):
      first_req = 1
      number_of_req = 1
      t1 = threading.Thread(target=auto_scale)
      t1.start()
    old_url = request.url
    parts = old_url.split("http://127.0.0.1:85")
    global cur_cont
    dict_container_lock.acquire()
    cur_cont = (cur_cont + 1) % len(dict_container)
    new_url = "http://127.0.0.1:"+str(cur_cont + 8000)+parts[1]
    dict_container_lock.release()
    resp = requests.request(
        method=request.method,
        url= new_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data())
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    number_of_req = number_of_req + 1
    no_of_locked_req.release()
    return response

def fault_tolerance():
    print("FAult tolereance started",file=sys.stderr)
    while(1):
        print("Fault tolerance running",file=sys.stderr)
        time.sleep(1)
        dict_container_lock.acquire()
        active_cont = list(dict_container.keys())
        for i in range(len(active_cont)):
            req = requests.get("http://127.0.0.1:"+str(active_cont[i])+"/api/v1/_health")
            if(req.status_code == 500):
                tmp = os.popen("docker kill " + dict_container[active_cont[i]]).read()
                del(dict_container[active_cont[i]])
                con = os.popen("docker run -p " + str(active_cont[i]) + ":80 -d -ti -v database:/db acts6").read()
#                con = os.popen("docker run -p " + str(active_cont[i]) + ":80 -d  acts").read()
                con_real = con.rstrip()
                dict_container[active_cont[i]] = con_real
                print("started a new container for "+str(active_cont[i]),file=sys.stderr)
        dict_container_lock.release()
        #sleep(60)
if __name__ == '__main__':
    init_container()
    t2 = threading.Thread(target = fault_tolerance)
    t2.start()
    app.run("0.0.0.0",port=85)
