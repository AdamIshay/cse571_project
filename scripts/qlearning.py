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
from matplotlib import pyplot as plt

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
        
        return q_values

    def task2(self, episodes):    
        q_values = {}
        # Your code here
        return q_values

    def task1(self, trajectories_json_file):
        q_values = {}
        # Your code here
        
 
        return q_values  

if __name__ == "__main__":

    args = parser.parse_args()

    if args.task == 1:
        QLearning(args.task, headless=args.headless, sample=args.sample)
    elif args.task == 2 or args.task == 3:
        QLearning(args.task, headless=args.headless, episodes=args.episodes)



    
