#!/usr/bin/env python
# encoding: utf-8

import rospy
from std_msgs.msg import String
import problem
import json
import os
import argparse
import numpy as np
import random
import environment_api as api
from matplotlib import pyplot as plt
import pdb
import re
from Agent import Agent

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-task', help="Task to execute:\n1. Q learning on sample trajectories\n2. Q learning without pruned actions\n3. Q learning with pruned actions", metavar='1', action='store', dest='task', default="1", type=int)
parser.add_argument("-sample", metavar="1", dest='sample', default='1', help="which trajectory to evaluate (with task 1)", type=int)
parser.add_argument('-episodes', help="Number of episodes to run (with task 2 & 3)", metavar='1', action='store', dest='episodes', default="1", type=int)
parser.add_argument('-headless', help='1 when running in the headless mode, 0 when running with gazebo', metavar='1', action='store', dest='headless', default=1, type=int)


class QLearning:

    def __init__(self, task, headless=1, sample=1, episodes=1):
        rospy.init_node('qlearning', anonymous=True)
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        
        self.books_json_file = root_path + "/books.json"
        self.books = json.load(open(self.books_json_file))
        self.helper = problem.Helper()
        self.helper.reset_world()

        self.headless = headless
        self.alpha = 0.3
        self.gamma = 0.9
        self.root_path = root_path

        if(task == 1):
            trajectories_json_file = root_path + "/trajectories{}.json".format(sample)
            q_values = self.task1(trajectories_json_file)
        elif(task == 2):
            q_values = self.task2(episodes)
        elif(task == 3):
            q_values = self.task3(episodes)

        with open(root_path + "/q_values.json", "w") as fout:
            json.dump(q_values, fout)

    def reward_prune(self,current_state,state_active,state_passive,action,action_items,tbot,tbot_other):
        #function that chooses to prune invalid actions (with large negative reward and no state change) or go through the api 
        through_api=True
        next_state=None
        reward=None
        
        if action!='moveF' and action!='pick':
            return through_api,next_state,reward
        
        if action=='pick':
            book_number=int(re.findall(r'\d+', action_items[0])[0])
            if book_number not in tbot.books:
                reward=self.book_penalty
                through_api=False
                next_state=current_state.copy()

        if action=='moveF':
            tbot_near=tbot.tbot_near(state_active,state_passive)
            if tbot_near==state_active[2]: #if another tbot is in the same direction that tbot_active is facing
                reward=self.bump_penalty
                through_api=False
                next_state=current_state.copy()
                

        return through_api,next_state,reward
    
    def choose_action(self, tbot,epsilon,state):
        if epsilon>np.random.uniform(): #if this, do random
            action_string=random.choice(api.get_all_actions())
            
        else:
            action_idx=tbot.q[state].argmax()
            action_string=tbot.idx_to_action(action_idx)
            
        action_split=action_string.split()
        action=action_split[0]
        action_items=action_split[1:]
        
        action_params={}
        for i,item in enumerate(self.action_reference[action]['params']):
            action_params[str(item)]=action_items[i]
        
        return action,action_items,action_params
    
    
    def task3(self, episodes):
        
        q_values = {}
        
        # Your code here
        
        
        actions_json_file='/action_config.json'

        with open(self.root_path + actions_json_file) as json_file:
            try:
                self.action_reference = json.load(json_file, parse_float=float)
            except (ValueError, KeyError, TypeError):
                print "JSON error"
        
        
        
        
        episodes=300
        episode_update=5 #the amount of episodes a tbot will train while the other tbots policy remains constant. must be a divisor of episodes
        
        
        epsilon_initial=.95
        epsilon_decay=.02
        epsilon_calc= lambda epsilon_initial,epsilon_decay,i: max(0.05, epsilon_initial - epsilon_decay*i) 
        
        self.book_penalty=-100
        self.bump_penalty=-100
        
        pdb.set_trace()
        
        #q tables initialized to zero 
        q1=np.zeros((4,4,4,2,2,4,5)) #(x,y, orientation, c1,c2,tbot_near,action) #c1,c2 will be zero if available, and one if picked up 
        q2=np.zeros((4,4,4,2,2,4,5))
        
        agent1_books=[1]
        agent2_books=[2]
        
        
        agent1=Agent('robot1',q1,agent1_books) 
        agent2=Agent('robot2',q2,agent2_books)
        
        tbot_list=[agent1,agent2]
        
        
        episode_block=int(episodes/episode_update)
        
        for i in range(episode_block):
          epsilon=epsilon_calc(epsilon_initial,epsilon_decay,i)
          for tbot in tbot_list: #determines which tbot is learning, active updates table, passive does not
            tbot_active=tbot
            tbot_passive_set=set(tbot_list)-set([tbot])
            tbot_passive=tbot_passive_set.pop()
            for e in range(episode_update):#cycle through the episodes inside an episode block
              api.reset_world()
              initial_state=api.get_current_state()
              current_state=initial_state
              
              state_active=tbot_active.dict_to_np_state(current_state,tbot_passive)  #active bots state tuple
              state_passive=tbot_passive.dict_to_np_state(current_state,tbot_active) #pssive bots state tuple
              
              while not api.is_terminal_state(current_state):
                
                through_api=True # flag for going through API for an action, if False, then reward is given manually


                #pick action for tbot_active
                #choose either random or exploit, according to epsilon=epsilon_calc(epsilon_initial, epsilon_decay, i)
                

                action_A,action_items_A,action_params_A=self.choose_action(tbot_active,epsilon,current_state)
                
                pdb.set_trace()
                
                
                through_api,next_state,reward=self.reward_prune(current_state,state_active,state_passive,action_A,action_items_A,tbot_active,tbot_passive)
                
                if through_api:
                  success,next_state=api.execute_action(action_A,action_params_A,tbot_active.name)
                  reward=api.get_reward(current_state,action_A,next_state)
                
                next_state_active=tbot_active.dict_to_np_state(next_state,tbot_passive)
                
                
                #update q_values of tbot_active ONLY
                pdb.set_trace()
                
                state_action_idx=tuple(state_active)+tuple(tbot_active.idx_to_action.index(action_A))
                tbot_active.q[state_action_idx]=(1-self.alpha)*tbot_active.q[state_action_idx]+self.alpha*(reward+self.gamma*max(tbot_active.q[next_state_active]))
                
                
                
                current_state=next_state # udpate current state for other tbot
                
                state_active=tbot_active.dict_to_np_state(current_state,tbot_passive)  #active bots state tuple
                state_passive=tbot_passive.dict_to_np_state(current_state,tbot_active) #pssive bots state tuple
        
        
        
                action_P,action_items_P,action_params_P=self.choose_action(tbot_passive,epsilon,current_state)
        
                through_api,next_state,reward=self.reward_prune(current_state,state_active,state_passive,action_A,action_items_A,tbot_active,tbot_passive) #reward won't be used 
                
        
        
        
                current_state=next_state # udpate current state for active tbot
                
                state_active=tbot_active.dict_to_np_state(current_state,tbot_passive)  #active bots state tuple
                state_passive=tbot_passive.dict_to_np_state(current_state,tbot_active) #pssive bots state tuple
        
        
        
        
        
        
        
        
        
        
        return q_values

    def task2(self, episodes):    
        q_values = {}
        # Your code here
        return q_values

    def task1(self, trajectories_json_file):
        q_values = {}
        # Your code here
        print(self.helper.get_all_actions())
        #print(self.helper.get_all_actions(2))
        api.execute_action('moveF', {}, 'robot1')
        #self.helper.execute_action('moveF', {}, 'robot2')
        
 
        return q_values  

if __name__ == "__main__":

    args = parser.parse_args()

    if args.task == 1:
        QLearning(args.task, headless=args.headless, sample=args.sample)
    elif args.task == 2 or args.task == 3:
        QLearning(args.task, headless=args.headless, episodes=args.episodes)