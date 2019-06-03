#!/bin/bash

###
#
# restore_code.sh: a script that destroys all changes in the ~/RaceYourCodeVIRTUAL/code directory.
#
# 2018-12-11
#
###


function ryc_restore {
	rm -r ~/RaceYourCodeVIRTUAL/code/*
	cp -r ~/RaceYourCodeVIRTUAL/assets/code_for_restore/* ~/RaceYourCodeVIRTUAL/code/
}

echo "Continuing will restore the ~/RaceYourCodeVIRTUAL/code directory back to its original state."
echo "*ALL* of your changes to the code in that directory will be lost."
echo
while true; do
    read -p "Do you wish to continue? " yn
    case $yn in
        [Yy]* ) echo "Restoring..."; ryc_restore; break;;
        [Nn]* ) echo "Quit."; sleep 2; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

read -p "Press ENTER to quit" junk
echo "Done."
sleep 2
