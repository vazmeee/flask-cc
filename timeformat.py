import datetime
def get_time()
    now=str(datetime.datetime.now())
    str=now[0:-7]
    d=str[8:10]
    mo=str[5:7]
    y=str[0:4]
    h=str[11:13]
    m=str[14:16]
    s=str[17:19]
    timestamp=d+'-'+mo+'-'+y+':'+s+'-'+m+'-'+h
    return timestamp

print(timestamp)
print(type(get_time()))
#print()
