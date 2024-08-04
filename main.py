import pygame as p
import time as t
import random as r
import math as m
import numpy as np
import array
from itertools import combinations
from ast import Num



p.font.init()
p.display.init()

Width,Hight = 950,950
gravity = 9.81
Collisions = 0
display = p.display.set_mode((Width,Hight))
p.display.set_caption("Ball Collisions Simulation by: Dagm Bisrat")


def dis(x1,y1,x2,y2):
    return m.sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))

class Ball:
    def __init__(self,box,x,y,size,color,fill=False,xspeed = r.uniform(-2.1, 2.1),yspeed = r.uniform(-3.3, 3.3)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.fill = fill
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.box = box

        self.r = p.math.Vector2((x, y))
        self.v = p.math.Vector2((xspeed, yspeed))





    def draw_(self,window):
        if self.fill == False:
            p.draw.circle(window,self.color, self.r,self.size)
        else:
            p.draw.circle(window,self.color, self.r ,self.size,2)



    def move(self):
            self.Collisions()
            self.r += self.v *  2.0




    def Collisions(self):
        if self.r.x + self.size >= self.box.x + self.box.size: #rigth of box Collision
            self.v.x = -1* self.v.x
        if self.r.x <= self.box.x+self.size: #left side of box Collision
            self.v.x = -1* self.v.x
        if self.r.y >= self.box.y + self.box.size-self.size: # top of box Collision
            self.v.y = -1* self.v.y
        if self.r.y <= self.box.y+self.size: # bottom of box Collision
            self.v.y = -1* self.v.y




def Collision_with_ball(ball,ball2):
    if ball.r.distance_to(ball2.r) <= ball.size + ball2.size:  #check if the two balls have collided
        print("Collisions")
        global Collisions
        Collisions += 1

        m1, m2 = ball.size**2, ball2.size**2 #initizees the mass of the two balls
        M = m1 + m2                          #initilaizes the total mass
        r1, r2 = ball.r, ball2.r             #initializs the point corinents of both balls
        d = np.linalg.norm(r1 - r2)**2       #initialises the dist betwwn the two vectors sqared
        v1, v2 = ball.v, ball2.v             #initalises the velocity vecters of both objects
        v1next = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)  #solves for the velocity vector after compleat elastic colliion for ball 1
        v2next = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)  #solves for the velocity vector after compleat elastic colliion for ball 2
        ball.v = v1next
        ball2.v = v2next

def randomball(box):
    rx = r.randrange(box.x +25 ,box.x + box.size-25)#random x value inside the box
    ry = r.randrange(box.y + 25 ,box.y + box.size-25)#random y value inside the box

    rsize = r.randrange(5,25)

    rcolor = (r.randrange(1,255),r.randrange(1,255),r.randrange(1,255))

    ball = Ball(box,rx,ry,rsize,rcolor,)

    return ball



class Box():
    def __init__(self,x = 75,y = 75,size=790,color =(0,0,225)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color


    def draw_(self):
        p.draw.line(display, self.color,(self.x,self.y),(self.x + self.size,self.y ))#top 1
        p.draw.line(display, self.color,(self.x + self.size,self.y ), (self.x + self.size,self.y + self.size))#right 1
        p.draw.line(display, self.color,(self.x ,self.y + self.size), (self.x + self.size,self.y + self.size))#bottom 3
        p.draw.line(display, self.color,(self.x,self.y),(self.x,self.y + self.size))#left 2



def main():
    run = True
    FPS = 60
    Clock = p.time.Clock()
    f = p.font.SysFont("Courier", 25,False,False)
    box = Box()


    numofballs = r.randrange(5,55)
    balls = []  #creates an array with a random scope

    for i in range(numofballs):
        balls.append(randomball(box)) #sets each index of the random array with a random ball







    def redraw():
        display.fill((0,0,0))

        lable = f.render("Fully Elastic Collisions Sim",True,(230,230,250))
        display.blit(lable, (Width/2 -200,20))

        c = f.render(f"Collisions:{Collisions}"  ,True,(230,230,250))
        display.blit(c, (40,Hight - 50))

        c = f.render(f"Balls:{numofballs}"  ,True,(230,230,250))
        display.blit(c, (Width - 150,Hight - 50))

        box.draw_()
        for i in range(numofballs):
            balls[i-1].draw_(display)
        p.display.update()






    while run:
        Clock.tick(FPS)
        redraw()

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False





            if  p.mouse.get_pos() != 0:   #checks if postion of the mouse is in the window
                for i in range(numofballs):   # itirates through the ball list
                    x,y = p.mouse.get_pos()
                    V = p.math.Vector2((x, y))
                    if balls[i].r.distance_to(V) <= balls[i].size:# checks if the mouse is in the area of each ball on the iist
                        balls[i].fill = True #unfills the ball that is being toched by the mouse
                        mouse_buttons = p.mouse.get_pressed()
                        if mouse_buttons[0]:  # Left mouse button
                            print("Left mouse button is being pressed")
                            balls[i].r = V
                    else:
                        balls[i].fill = False


            keys=p.key.get_pressed()

            if keys[p.K_UP] | keys[p.K_KP_PLUS]: #checks if "up arrow" or "+" botton is clicked
                    print("added")
                    numofballs += 1
                    balls.append(randomball(box)) #adds a ball when clicked

            if keys[p.K_DOWN] | keys[p.K_KP_MINUS]: #checks if "down arrow" or "-" is clicked
                if  numofballs > 0:
                    print("removed")
                    numofballs -= 1
                    balls.pop(numofballs -1) #removes a ball if clicked




        for i in range(numofballs): #moves every ball according to its velocity
            balls[i-1].move()

        pairs = combinations(range(numofballs), 2) #iterates through every possible unique pairs in the array
        for i,j in pairs:
            Collision_with_ball(balls[i],balls[j])#checks the pairs for collision one by one







main()
