# group_8

#IMPORTANT NOTES BEFORE RUNNING
- SIMULATION DOES NOT WORK IF TRAINING HAS NOT COMPLETED
- SIMULATION USUALLY HALTS AFTER TAKING THE FIRST FEW STEPS OR AFTER COLLECTING THE FIRST BOOK, THE REASON FOR THIS MAY BE GAZEBO
- TRAINING WITH '-b 1' TOOK APPROXIMATELY 1 HOUR, WHILE TRAINING WITH '-b 3' TOOK APPROXIMATELY 8 HOURS ON A FAST PC.



First we need to train the model by updating the Q tables, then we can run the simulation. 
Every command below this point should be run in a separate terminal. When you train, the Q table of each tbot will be saved, as well as the cumulative reward, like in homework #3.

First run each of these commands to download the code and give permissions. If you are not downloading from Github then skip the following line.

cd ~/catkin_ws/src && git clone https://github.com/AdamIshay/group_8.git

chmod u+x ~/catkin_ws/src/group_8/scripts/*.py

chmod u+x ~/catkin_ws/src/group_8/env_setup.sh && ~/catkin_ws/src/group_8/env_setup.sh



		roscore



if running with 1 book for each tbot:

	
	if training: #REQUIRED FOR SIMULATION IMMEDIATELY BELOW

		rosrun cse571_project server.py -sub 1 -b 1 -s 32 -t 1

		rosrun cse571_project qlearning.py -task 2 -episodes 450

	if running simulation: #DOES NOT WORK UNLESS TRAINING IMMEDIATELY ABOVE WAS COMPLETED
		#NOTE ON SIMULATION: SIMULATION USUALLY HALTS AFTER TAKING THE FIRST FEW STEPS OR AFTER COLLECTING THE FIRST BOOK
		rosrun cse571_project server.py -sub 1 -b 1 -s 32 -t 0

		rosrun cse571_project move1_bot3.py --> for first bot

		rosrun cse571_project move2_bot3.py --> for second bot
		
		roslaunch cse571_project maze.launch

		rosrun cse571_project qlearning.py -task 3 -episodes 0

if running with 3 books for each tbot:
	

	if training: #REQUIRED FOR SIMULATION IMMEDIATELY BELOW

		rosrun cse571_project server.py -sub 1 -b 3 -s 32 -t 1
	
		rosrun cse571_project qlearning.py -task 4 -episodes 450

	if running simulation: #DOES NOT WORK UNLESS TRAINING IMMEDIATELY ABOVE WAS COMPLETED

		rosrun cse571_project server.py -sub 1 -b 3 -s 32 -t 0

		rosrun cse571_project move1_bot3.py --> for first bot

		rosrun cse571_project move2_bot3.py --> for second bot
		
		roslaunch cse571_project maze.launch

		rosrun cse571_project qlearning.py -task 5 -episodes 0



