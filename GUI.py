import pygame
pygame.init()
pygame.scrap.init()

class Text(pygame.Surface):
    def __init__(self,display,rect=(0,0,1,1),text='',size=75,fg=(0,0,0)):
        W,H=display.get_size()
        rect=[int(v*(W,H)[i%2]) for i,v in enumerate(rect)]
        pygame.Surface.__init__(self,rect[2:],pygame.SRCALPHA)
        self.display=display
        self.pos=rect[:2]
        self.text=text
        self.fg=fg
        self.font=pygame.font.SysFont('courier',size)
        self.render()
    def render(self):
        txt=self.font.render(self.text,True,self.fg)
        W,H=self.get_size()
        w,h=txt.get_size()
        self.text_pos=((W-w)//2,(H-h)//2)
        self.blit(txt,self.text_pos)
    def place(self):
        self.display.blit(self,self.pos)

class Button(Text):
    def __init__(self,display,rect=(0,0,1,1),text='',size=75,pbg=(50,50,50),pfg=(200,200,200),abg=(150,150,150),afg=(100,100,100)):
        self.pbg=pbg
        self.pfg=pfg
        self.abg=abg
        self.afg=afg
        self.a=False
        Text.__init__(self,display,rect,text,size,pfg)
    def render(self):
        pygame.draw.rect(self,self.abg if self.a else self.pbg,(0,0,*self.get_size()),0,20)
        Text.render(self)
    def is_pressed(self,events):
        x,y=pygame.mouse.get_pos()
        X,Y=self.pos
        w,h=self.get_size()
        a=self.a
        self.a=X<x<X+w and Y<y<Y+h
        if a!=self.a:
            self.fg=self.afg if self.a else self.pfg
            self.render()
        if not self.a:return False
        for ev in events:
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:return True
        return False
class ListBox(Button):
    def __init__(self,display,rect=(0,0,1,1),texts=(''),size=75,pbg=(50,50,50),pfg=(200,200,200),abg=(150,150,150),afg=(100,100,100)):
        self.A = False
        Button.__init__(self,display,rect,texts[0],size,pbg,pfg,abg,afg)
        y=rect[1]
        h=rect[3]
        self.list=[]
        for txt in texts:
            y+=h
            self.list.append(Button(display,(rect[0],y,rect[2],rect[3]),txt,size,abg,afg,pbg,pfg))
    def render(self):
        Button.render(self)
        if self.A:
            for i in self.list:i.render()
    def place(self):
        Button.place(self)
        if self.A:
            for i in self.list:i.place()
    def events(self,events):
        prs=self.is_pressed(events)
        if prs:self.A=True
        if self.A:
            for i in self.list:
                if i.is_pressed(events):
                    self.text=i.text
                    self.render()
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and not prs: self.A = False
class Input(Text):
    def __init__(self,display,rect=(0,0,1,1),text='',size=75,fg=(0,0,0),bg_text='',bg_fg=(200,200,200),limit=21):
        self.limit = limit
        self.p = -1
        self.bg_text=Text(display,rect,bg_text,size,bg_fg)
        Text.__init__(self,display,rect,text,size,fg)
    def render(self):
        self.fill((0,0,0,0))
        Text.render(self)
        pygame.draw.rect(self,self.fg,(0,0,*self.get_size()),2,20)
        if self.p!=-1:
            x=self.text_pos[0]+self.p*self.font.get_height()/1.9
            h=self.font.get_height()
            y=(self.get_height()-h)/2
            pygame.draw.line(self,self.fg,(x,y),(x,y+h))
    def place(self):
        Text.place(self)
        if len(self.text)<1 and self.p==-1:self.bg_text.place()
    def events(self,events):
        x,y=pygame.mouse.get_pos()
        X,Y=self.pos
        w,h=self.get_size()
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if X<x<X+w and Y<y<Y+h:
                    self.p = round((x - self.text_pos[0] - X) / (self.font.get_height()/1.9))
                    self.p = max(0, min(len(self.text), self.p))
                else:self.p=-1
                self.render()
        if self.p!=-1:
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    if ev.key==1073742049:continue
                    elif ev.key == pygame.K_LEFT:
                        self.p-=1
                    elif ev.key == pygame.K_RIGHT:
                        self.p+=1
                    elif ev.key == 8:
                        self.text = self.text[:max(self.p - 1,0)] + self.text[self.p:]
                        self.p-=1
                    elif len(self.text)<self.limit:
                        self.text=self.text[:self.p]+ev.unicode+self.text[self.p:]
                        self.p+=1
                    self.p=max(0,min(len(self.text),self.p))
                    self.render()