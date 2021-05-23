import pygame
from online import *
from random import randint
import server
from GUI import *
from os import listdir,mkdir,remove
import sys
try:
    font=pygame.font.SysFont('courier',15)
    def write(name,pos,k):
        txt=font.render(name,True,(0,0,0))
        x,y=pos;y-=k
        w,h=txt.get_size()
        display.blit(txt,(x-w//2,y-h//2))
    def add_server(ip,port,name,tp):
        global y
        servers.append(Button(display, (0.17, y, 0.74, 0.075), f'{name}{" " * (30 - len(name)-len(ip)-len(port))}{ip}:{port}'))
        servers[-1].tp=tp
        servers[-1].ip=ip
        servers[-1].port=port
        servers[-1].name=name
        servers.append(Button(display, (0.92, y, 0.05, 0.075), 'X'))
        y+=0.1
    W,H=1920,1080
    display=pygame.display.set_mode((W,H))
    pygame.display.set_caption('snake online')
    scene='menu()'
    nick=''
    servers=[]
    scroll=0
    client=None
    try:listdir('servers')
    except:mkdir('servers')
    y=0.05
    for S in listdir('servers'):
        try:
            ip,port,name,tp=S.split()
            tp=int(tp)
            add_server(ip,port,name,tp)
            if tp:server.add_server(name,ip,port)
        except:pass
    def menu():
        global scene,nick
        name=Input(display,(0.3,0.35,0.4,0.1),nick,bg_text='nickname',limit=15)
        label = Text(display, (0, 0, 1, 0.2), 'snake online', 200, (0, 255, 0))
        create=Button(display,(0.3,0.5,0.4,0.1),'add server')
        join=Button(display,(0.3,0.65,0.4,0.1),'join game')
        ext=Button(display,(0.3,0.85,0.4,0.1),'quit')
        while scene=='menu()':
            events=pygame.event.get()
            if create.is_pressed(events):scene='create()'
            if join.is_pressed(events):scene='join()'
            if ext.is_pressed(events):exit()
            name.events(events)
            display.fill((255,255,255))
            label.place()
            create.place()
            join.place()
            ext.place()
            name.place()
            nick=name.text
            pygame.display.flip()
    def create():
        global scene
        label = Text(display, (0, 0, 1, 0.2), 'snake online', 200, (0, 255, 0))
        name=Input(display,(0.4,0.4,0.55,0.1),bg_text='server name',limit=9)
        ip=Input(display,(0.4,0.55,0.55,0.1),bg_text='ip:port')
        back = Button(display, (0.05, 0.4, 0.2, 0.1), 'back')
        crt=Button(display,(0.05,0.55,0.2,0.1),'add')
        while scene=='create()':
            events=pygame.event.get()
            ip.events(events)
            if back.is_pressed(events):scene='menu()'
            if crt.is_pressed(events):
                try:
                    Ip,port=ip.text.split(':')
                    tp=int(Ip in IPs())
                    with open(f'servers/{Ip} {port} {name.text} {tp}','w'):pass
                    add_server(Ip,port,name.text,tp)
                    server.add_server(name.text,Ip,port)
                except:pass
                scene='menu()'
            name.events(events)
            display.fill((255,255,255))
            label.place()
            ip.place()
            back.place()
            crt.place()
            name.place()
            pygame.display.flip()
    def join():
        global scene,y,client
        back = Button(display, (0.01, 0.05, 0.15, 0.1), 'back')
        while scene=='join()':
            events=pygame.event.get()
            for serv in servers:
                if serv.is_pressed(events):
                    if serv.text=='X':
                        I=servers.index(serv)-1
                        s=servers[I]
                        ip,port,name,tp=s.ip,s.port,s.name,s.tp
                        remove(f'servers/{ip} {port} {name} {tp}')
                        servers.pop(I)
                        servers.pop(I)
                        y-=0.1
                        for i in range(I,len(servers)):servers[i].pos[1]-=H/10
                        if tp:server.del_server(name)
                    else:
                        client=Client((serv.ip,int(serv.port)))
                        scene='play()'
            if back.is_pressed(events):scene='menu()'
            display.fill((255,255,255))
            for serv in servers:serv.place()
            back.place()
            pygame.display.flip()
    def play():
        global nick,scene
        t=randint(0,3)
        k=20
        if nick=='':nick='player'
        client.send('player')
        (x, y), snakes,names = eval(client.get())
        while scene=='play()':
            for ev in pygame.event.get():
                if ev.type==pygame.KEYDOWN:
                    if ev.key==pygame.K_RIGHT:t=0
                    if ev.key==pygame.K_LEFT:t=2
                    if ev.key==pygame.K_DOWN:t=1
                    if ev.key==pygame.K_UP:t=3
            display.fill((255,255,255))
            client.send(str(t))
            (x,y),snakes,names=eval(client.get())
            pygame.draw.rect(display,(0,255,0),(x*k,y*k,k,k))
            for snake in snakes.values():
                for x,y in snake:
                    pygame.draw.rect(display,(0,0,255),(x*k,y*k,k,k))
                write(nick,snake[0],k)
            pygame.display.flip()

    while True:exec(scene)
except:pygame.quit()