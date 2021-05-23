from threading import Thread
from random import choice,randint
from online import *
from time import *

servers={}
def del_server(name):
    servers[name].join(0)
    servers.pop(name)
def add_server(name,ip,port):
    servers[name]=Thread(target=start,args=(ip,port))
    servers[name].start()
def start(ip,port):
    def go():
        nonlocal snakes,t,meal
        while True:
            T=time()
            keys=tuple(snakes.keys())
            dl=[]
            for key in keys:
                for i in range(len(snakes[key])-1,0,-1):snakes[key][i]=snakes[key][i-1].copy()
                snakes[key][0][0]=(snakes[key][0][0]+v[t[key]][0])%len(mp[0])
                snakes[key][0][1]=(snakes[key][0][1]+v[t[key]][1])%len(mp)
                if tuple(snakes[key][0])==meal:
                    snakes[key].append(snakes[key][-1])
                    meal=get_pos()
                m = 0
                if len(snakes[key])==2:m-=(snakes[key][0]==snakes[key][1])
                for k in keys:m+=snakes[k].count(snakes[key][0])
                if m>1:dl.append(key)
            for k in dl:
                snakes.pop(k)
                t.pop(k)
            sleep(max(0,0.1-(time()-T)))
    def get_pos():
        nonlocal mp
        v=set()
        for y in range(len(mp)):
            for x in range(len(mp[y])):
                v.add((x,y))
        for snake in snakes.values():
            for X,Y in snake:
                v.discard((X,Y))
        return choice(list(v))
    snakes={}
    name={}
    v=((1,0),(0,1),(-1,0),(0,-1))
    t={}
    W,H=1920,1080
    k=20
    mp=[[0]*(W//k) for _ in range(H//k)]
    meal=get_pos()
    server=Server(ip,port)
    Thread(target=go).start()
    while True:
        data,addres=server.get()
        try:
            if data in '0123':t[addres]=int(data)
            else:
                name[addres]=data
                x, y = get_pos()
                snakes[addres] = [[x, y]]
                t[addres]=randint(0,3)
        except:pass
        server.send(str((meal,snakes,name)),addres)