import docker
import time
from threading import Thread, currentThread, active_count
from flask import Flask, redirect
import requests

app = Flask(__name__)
client = docker.from_env()

container_list = list()

last_address =  8000
last_container_index = 0 

no_of_requests_in_last_two_mins = 0

# client.containers.run("spacevim/spacevim:latest", detach=True, ports = {'2222/tcp': 3333})

def get_container_ip(container):
    l = list(container.attrs['HostConfig']['PortBindings'].values())
    return l[0][0]['HostPort']

def restart_container(container):
    ip = get_container_ip(container)
    container.stop()
    container_list_pos = container_list.index(container)
    container_list.remove(container)
    container_new = client.containers.run('spacevim/spacevim:latest', detach=True, ports = {'80/tcp':ip})        
    container_list.insert(container)

def provision_containers(n):
    print("provisioning container ", n)
    global last_address
    for i in range(n):
#        container_new = client.containers.run('acts:latest', detach=True, ports = {'80/tcp':last_address})        
        container_new = client.containers.run("spacevim/spacevim:latest", detach=True, ports = {'80/tcp': last_address})
        print("provisioned container with ip ", last_address)
        last_address += 1
        container_list.append(container_new)

def delete_containers(n):
    print("deleting container ", n)
    for i in range(n):
        container = container_list.pop() 
        container.stop()

# returns the ip address of the right container
def load_balancer_handler():
    if(len(container_list) != 0):
        return "" 
    container = container_list[last_container_index]
    last_container_index += 1
    last_container_index %= len(container_list)
    return get_container_ip(container)

def fault_tolerance_handler():
    while(1):
        time.sleep(1)
        for container in container_list:
            ip = get_container_ip(container)
            print('0.0.0.0:'+str(ip)+'/api/v1/_health')
#            r = requests.get('0.0.0.0:'+str(ip)+"/api/v1/_health")
#            status_code = r.status_code()
#            if(status_code == 500):
#                restart_container(container)

def auto_scaling_handler():
    print("autoscaling_handler",int(no_of_requests_in_last_two_mins/20)+1)
    while(1):
        bracket = int(no_of_requests_in_last_two_mins/20)+1 
        if(len(container_list) < bracket):
            provision_containers(bracket-len(container_list))
#            Thread(target = provision_containers, args=(bracket-len(container_list), )).start()
        elif(len(container_list) > bracket):
            delete_containers(len(container_list)-bracket)
        else:
            print("No need of new containers")
        time.sleep(10)

@app.route("/<path:path>")
def redirect_to_other_containers():
    no_of_requests_in_last_two_mins+=1
    container_ip = load_balance_handler()
    return redirect('0.0.0.0:'+container_ip+"/"+path, code=302)

if __name__ == '__main__':
#    Thread(target=app.run).start()
#    Thread(target=useless).start()
    Thread(target=fault_tolerance_handler, daemon=True).start()
    Thread(target=auto_scaling_handler, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
    print("Current Thread count: %i." % active_count())
