#!/bin/bash

###
#
# runsimulator.sh: a script that deals with running the code for the virtual robot, and running the simulation.
#
# 2018-12-11
#
###

echo "Running simulation script. Hit Ctrl+Z when finished."
# Run the simulation
cd ~/RaceYourCodeVIRTUAL/code/Simulation
# Run the simulator in the background, pipe stderr to stdout, pipe all stdout to /dev/null
java -jar Sim.jar > /dev/null 2>&1 &

python ~/RaceYourCodeVIRTUAL/code/SimulationFull.py
# Run the robot code
while [ $? -eq 75 ]
do
	python ~/RaceYourCodeVIRTUAL/code/SimulationFull.py
done
# Code doesn't exit nicely. Kill it instead
killall python

read -p "Press ENTER to quit" junk
echo "Done."
