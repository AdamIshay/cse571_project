#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:56:01 2019

@author: cse-571
"""

import numpy as np
import pdb 

    

#q table is (x,y,c1,c2,tbot_near,num_actions)

class Agent:
    def __init__(self,name,q):
        
        self.name=name
        self.q=q
        
        self.c=0
        
        #self.reward_key=reward_key
        #self.reward_locs=grid_rewards
        
        self.o_to_idx={'NORTH':0,'EAST':1, 'SOUTH':2, 'WEST': 3} #orientation to idx in state
        self.pos_to_idx=lambda n:int(n/.5)
        
        self.idx_to_action=['moveF', 'TurnCW', 'TurnCCW', 'pick book_1', 'pick book_2']
        
        
    def dict_to_np(self,d,other_bot):
        
        c1x=d['book_1']['x']
        c1y=d['book_1']['y']
        
        c2x=d['book_2']['x']
        c2y=d['book_2']['y']
        
        
        rx=self.pos_to_idx(d[self.name]['x'])
        ry=self.pos_to_idx(d[self.name]['y'])
        ro=self.o_to_idx[d[self.name]['orientation']]
        
        
        rx_other=self.pos_to_idx(d[other_bot.name]['x'])
        ry_other=self.pos_to_idx(d[other_bot.name]['y'])
        ro_other=self.o_to_idx[d[other_bot.name]['orientation']]
        
        
        
        
        tbot_near=self.tbot_near([rx,ry],[rx_other,ry_other])
        
        pdb.set_trace()
        
        
        state=(rx,ry,self.c,other_bot.c,tbot_near)
        
        
    def tbot_near(self,r1,r2):
        pdb.set_trace()
        if abs(r1[0]-r2[0])+abs(r1[1]-r2[1])==1:
            if r1[1]>r2[1]:
                return 2
            if r2[1]>r1[1]:
                return 0
            if r1[0]>r2[0]:
                return 3
            if r2[0]>r1[0]:
                return 1
            
        else:
            return 5
            
            
        


# =============================================================================
# s={u'book_1': {u'placed': False, u'x': 0.75, u'y': 3.0},
#  u'book_2': {u'placed': False, u'x': 0.75, u'y': 1.5},
#  u'robot1': {u'orientation': u'EAST', u'x': 1.0, u'y': 1.0},
#  u'robot2': {u'orientation': u'EAST', u'x': 1.0, u'y': 1.0}}
#     
# 
# a=Agent('robot1',1,1,1)
# a.dict_to_np(s,'robot2')
# 
# 
# 
# a=Agent('robot2',1,1,1)
# a.dict_to_np(s,'robot1')
# 
# =============================================================================
