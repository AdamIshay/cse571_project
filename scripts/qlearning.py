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


    def task3(self, episodes):
        
        q_values = {}
        
        # Your code here
        
        
        actions_json_file='/action_config.json'

        with open(self.root_path + actions_json_file) as json_file:
            try:
                action_reference = json.load(json_file, parse_float=float)
            except (ValueError, KeyError, TypeError):
                print "JSON error"
        
        
        
        
        episodes=300
        episode_update=5 #the amount of episodes a tbot will train while the other tbots policy remains constant. must be a divisor of episodes
        
        
        epsilon_initial=.95
        epsilon_decay=.02
        epsilon_calc= lambda epsilon_initial,epsilon_decay,i: max(0.05, epsilon_initial - epsilon_decay*i) 
        
        
        
        pdb.set_trace()
        
        #q tables initialized to zero 
        q1=np.zeros((4,4,2,2,4,5)) #(x,y,c1,c2,tbot_near,action) #c1,c2 will be zero if available, and one if picked up 
        q2=np.zeros((4,4,2,2,4,5))

        agent1=Agent('robot1',q1) 
        agent2=Agent('robot2',q2)
        
        tbot_list=[agent1,agent2]
        initial_state=api.get_current_state()
        
        
        
        
        for i in range(int(episodes/episode_update)):
          epsilon=epsilon_calc(epsilon_initial,epsilon_decay,i)
          for tbot in tbot_list:
            for e in range(episode_update):
              #pick action
              #choose either random or exploit, according to epsilon=epsilon_calc(epsilon_initial, epsilon_decay, i)
              
              if epsilon>np.random.uniform(): #if this, do random
                  action_string=random.choice(api.get_all_actions())
                  
              else:
                  action_idx=tbot.q[state].argmax()
                  action_string=tbot.idx_to_action(action_idx)
                  
              action_split=action_string.split()
              action=action_split[0]
              action_items=action_split[1:]
                
              action_params={}
              for i,item in enumerate(action_reference[action]['params']):
                  action_params[str(item)]=action_items[i]
              
              success,next_state=api.execute_action(action,action_params,tbot.name)
              
              #print("tbot reward key is " + str(tbot.reward_key))
              #get reward
              reward=get_reward(action,tbot,tbot_list)
              #get_reward(tbot
              
              #update q_values of ONLY tbot
              tbot.q[tuple(state)+tuple(action)]=(1-self.alpha)*tbot.q[tuple(state)+tuple(action)]+self.alpha*(reward+self.gamma*max(tbot.q[next_state]))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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



    
