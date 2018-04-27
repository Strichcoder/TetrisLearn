#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:15:19 2018

@author: gregorbachmann
"""

import numpy as np
import matplotlib.pyplot as plt

class blocks:
    def __init__(self, shape ,pos=[0,5],orientation=0):
        self.pos = pos
        self.shape = shape
        self.orientation = orientation
        
    
    def get_matrix(self):
        if self.shape==0: #STICK
            if self.orientation==0 or self.orientation==2:
                A = np.ones((1,4))
                self.ground=1
                self.side=4
            if self.orientation==1 or self.orientation==3:
                A = np.ones((4,1))
                self.ground=4
                self.side=1
        
        if self.shape==1: #TRIANGLE
            if self.orientation==0:
                A = np.zeros((2,3))
                A[1,0:3] = 1
                A[0,1] = 1
                self.ground = 2
                self.side=3
            if self.orientation==1:
                A = np.zeros((3,2))
                A[0:3,0] = 1
                A[1,1] = 1
                self.ground=3
                self.side=2
            if self.orientation==2:
                A = np.zeros((2,3))
                A[0,0:3] = 1
                A[1,1] = 1
                self.ground=2
                self.side=3
            if self.orientation==3:
                A = np.zeros((3,2))
                A[0:3,1] = 1
                A[1,0] = 1
                self.ground=3
                self.side=2
            
        if self.shape==2: #LEFT L
            if self.orientation==0:
                A = np.zeros((2,3))
                A[1,0:3] = 1
                A[0,0] = 1
                self.ground=2
                self.side=3
            if self.orientation==1:
                A = np.zeros((3,2))
                A[0:3,0] = 1
                A[0,1] = 1
                self.ground=3
                self.side=2
            if self.orientation==2:
                A = np.zeros((2,3))
                A[0,0:3] = 1
                A[1,2] = 1
                self.ground=2
                self.side=3
            if self.orientation==3:
                A = np.zeros((3,2))
                A[0:3,1] = 1
                A[2,0] = 1
                self.ground=3
                self.side=2
        
        if self.shape==3: #RIGHT L
            if self.orientation==0:
                A = np.zeros((2,3))
                A[1,0:3] = 1
                A[0,2] = 1
                self.ground=2
                self.side=3
            if self.orientation==1:
                A = np.zeros((3,2))
                A[0:3,0] = 1
                A[2,1] = 1
                self.ground=3
                self.side=2
            if self.orientation==2:
                A = np.zeros((2,3))
                A[0,0:3] = 1
                A[1,0] = 1
                self.ground=2
                self.side=3
            if self.orientation==3:
                A = np.zeros((3,2))
                A[0:3,1] = 1
                A[0,0] = 1
                self.ground=3
                self.side=2
        
        if self.shape==4: #LEFT S
            if self.orientation==0 or self.orientation==2:
                A = np.zeros((2,3))
                A[0,1:3] = 1
                A[1,0:2] = 1
                self.ground=2
                self.side=3
            if self.orientation==1 or self.orientation==3:
                A = np.zeros((3,2))
                A[0:2,0] = 1
                A[1:3,1] = 1
                self.ground=3
                self.side=2
        
        if self.shape==4: #RIGHT S
            if self.orientation==0 or self.orientation==2:
                A = np.zeros((2,3))
                A[0,0:2] = 1
                A[1,1:3] = 1
                self.ground=2
                self.side=3
            if self.orientation==1 or self.orientation==3:
                A = np.zeros((3,2))
                A[0:2,1] = 1
                A[1:3,0] = 1
                self.ground=3
                self.side=2
        
        if self.shape==5: #SQUARE
            A = np.ones((2,2))
            self.ground=2
            self.side=2
        return A
 

class tetris:
    sizeX=10
    sizeY=10
    block=blocks(2)
    field=np.zeros((sizeX,sizeY))
    
    def __init__(self,sizeX=10,sizeY=10):
        self.sizeX=sizeX
        self.sizeY=sizeY
        self.field=np.zeros((sizeX,sizeY))
    
    def rotate(self):
        self.block.orientation+=1
        self.block.orientation=self.block.orientation%4
        A=self.block.get_matrix()
        
        if self.block.shape==0 and (self.block.orientation==0 or self.block.orientation==2):
            self.block.pos[1]+=1
        if self.block.shape==0 and (self.block.orientation==1 or self.block.orientation==3):
            self.block.pos[1]-=1
        if self.check_if_valid():
            self.block.orientation-=1
            self.block.orientation=self.block.orientation%4
            A=self.block.get_matrix()

        return(self)
    
    def translate_left(self):
        self.block.pos[1]-=1
        if self.check_if_valid():
            self.block.pos[1]+=1
        return(self) 
     
    def translate_right(self):
        self.block.pos[1]+=1
        if self.check_if_valid():
            self.block.pos[1]-=1
        return(self) 
     
    def gravitate(self):
        self.block.pos[0]+=1
        if self.check_if_valid():
            A = self.block.get_matrix()
            self.clean()
            self.field[self.block.pos[0]:(self.block.pos[0]+A.shape[0]),self.block.pos[1]:(self.block.pos[1]+A.shape[1])]-=A
            self.new_block()
            self.delete_row()
        
    
    def check_if_valid(self):
        A = self.block.get_matrix()
        i_0 = A.shape[0]
        j_0 = A.shape[1]
        if self.block.pos[1]<0 or self.block.pos[1]+self.block.side>self.field.shape[1] or self.block.pos[0]<0 or self.block.pos[0]+self.block.ground>self.field.shape[0]-1:
            return True
        else:
            for i in range(0,i_0):
                for j in range(0,j_0):
                    if self.field[self.block.pos[0]+i+1,self.block.pos[1]+j]==-1 and A[i,j]==1:
                        #self.block.pos[0]-=1
                        return True
        return False
    
    
    def new_block(self):
        s=np.random.randint(0,6)
        r=np.random.randint(0,3)
        self.block=blocks(shape=s,orientation=r,pos=[0,5])
        if self.check_if_valid():
            self.block=None
            print('YOU LOST, could not generate any more blocks')
            return False
        else:
            return True
    
    def delete_row(self):
        for i in range(self.field.shape[1]):
            if np.sum(m.field[i,:])==-10:
                print('totally full')
                self.field=np.delete(self.field,i,axis=0)
                self.field=np.insert(self.field,0,0,axis=0) 
    
    def clean(self):
        for i in range(0,self.field.shape[0]):
            for j in range(0,self.field.shape[1]):
                if self.field[i,j]==1:
                    self.field[i,j]=0
    def project(self):
        self.clean()
        A = self.block.get_matrix()
        self.field[self.block.pos[0]:(self.block.pos[0]+A.shape[0]),self.block.pos[1]:(self.block.pos[1]+A.shape[1])]+=A
        
    def draw(self):
        plt.matshow(self.field)