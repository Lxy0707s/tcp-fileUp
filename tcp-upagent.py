#! /usr/bin/python
# encoding:utf-8
import json
import socket
import os
import time

metrics = []
remote_addr = '192.168.37.100'
port = 8080
filename = "/usr/local/tcp-fileUp/data"
f = open(filename, 'rb')
filesize = str(os.path.getsize(filename))
path, file_name = os.path.split(filename)
start = 0.0
time_cost = 0
code = 0
#print filesize


# 获取主机名
def hostname():
    sys = os.name
    if sys == 'nt':
        return os.getenv('computername')
    elif sys == 'posix':
        host = os.popen('echo $HOSTNAME')
        try:
            return host.read()
        finally:
            host.close()
    else:
        return 'Unkwon hostname'


def generate_metric(cost_time, codes):
    # print "metric 生成上报"
    host = hostname()
    global metrics
    metric_json = {
        "name": "tcp_up_file_prob",
        "time": int(time.time()),
        "value": 0,
        "tags": {
            "endpoint": host,
            "file_name": "data",
            "file_size": "1k",
            "target": remote_addr
        },
        "fields": {
            "cost_time": cost_time,
            "flag": codes
            },
        "step": 60,
    }
    metrics.append(metric_json)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect((remote_addr, port))

while True:
    try:
        start = time.time()
        for line in f:
            s.send(line)
#            print('client data sending...')
        s.send(b'end')
        break
    except socket.timeout or socket.error:
        code = 1
        continue

s.close
end = time.time()
time_cost = round(end - start, 4)
#print('cost' + str(time) + 's')
generate_metric(time_cost, code)
print(json.dumps(metrics))
