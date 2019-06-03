#!/bin/bash

# Settings
ONLINE="https://raw.githubusercontent.com/piborg/ryc-help/master/GettingStarted.pdf"
FILENAME="RaceYourCodeVIRTUAL_GettingStarted.pdf"
BACKUP="RaceYourCodeVIRTUAL_GettingStarted.pdf.old"
UPDATED="GettingStarted.pdf"

# Attempt to download a new copy
cd /home/ryc_6/RaceYourCodeVIRTUAL/instructions
rm $UPDATED
wget $ONLINE

# Move files if a new copy was downloaded
if [ -f $UPDATED ]; then
	rm $BACKUP
	mv $FILENAME $BACKUP
	mv $UPDATED $FILENAME
	echo "New copy of $FILENAME was downloaded"
else
	echo "Using old copy of $FILENAME"
fi

# Open the file
xdg-open $FILENAME

read -p "Press Enter to close terminal and PDF."

