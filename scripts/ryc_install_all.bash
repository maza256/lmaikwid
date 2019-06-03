#!/bin/bash

###
#
# ryc_install_all.bash: install script for the Rolls-Royce Race Your Code laptops.
#
# 2018-12-11
#
###

# Install what we need for the simulation to run
sudo apt update
sudo apt -y upgrade

# General
sudo apt -y install default-jre vlc geany
# For opencv to run with python
sudo apt -y install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
# For modifying the desktop icons for them to work
sudo apt -y install --no-install-recommends gnome-panel

# Get PiBorg code
git clone https://git.code.sf.net/p/rr-rycv/code RaceYourCodeVIRTUAL

# Sort out the files
ryc_USERNAME=`whoami`
read -p "Enter FTP password for $ryc_USERNAME: " ryc_FTPPASSWORD
echo "FTP password is $ryc_FTPPASSWORD"

sed -i.bak s/rycFTPPASSWORD/$ryc_FTPPASSWORD/g ~/RaceYourCodeVIRTUAL/scripts/ftp_upload.sh
sed -i.bak s/rycUSERNAME/$ryc_USERNAME/g ~/RaceYourCodeVIRTUAL/assets/Desktop/*.desktop
sed -i.bak s/rycUSERNAME/$ryc_USERNAME/g ~/RaceYourCodeVIRTUAL/scripts/*.sh
rm ~/RaceYourCodeVIRTUAL/assets/Desktop/*.desktop.bak
mv ~/RaceYourCodeVIRTUAL/assets/Desktop ~/
echo "Organised files."

echo "Please edit the desktop shortcuts (but don't actually make changes)."
# Now edit each desktop shortcut with gnome-desktop-item-edit to make them able to run
gnome-desktop-item-edit ~/Desktop/*.desktop

# Download, build and install OpenCV (we need a specific version not in repos)
cd ~/Downloads/
wget https://github.com/opencv/opencv/archive/2.4.13.6.zip
mkdir /home/$ryc_USERNAME/RaceYourCodeVIRTUAL/opencvbuild
unzip 2.4.13.6.zip -d ~/RaceYourCodeVIRTUAL/opencvbuild/
cd ~/RaceYourCodeVIRTUAL/opencvbuild
# This will take a while! (~1 hour)
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ~/RaceYourCodeVIRTUAL/opencvbuild/opencv-2.4.13.6/
make
sudo make install

#echo "Running the simulation..."
# Run the simulation
#cd ~/RaceYourCodeVIRTUAL/code/Simulation
# Run the simulator in the background, pipe stderr to stdout, pipe the lot to /dev/null
#java -jar Sim.jar > /dev/null 2>&1 &
# Run the robot code
#gnome-terminal -x sh -c "echo 'Press Enter when the simulator is ready:' ; read response ; python ~/RaceYourCodeVIRTUAL/code/SimulationFull.py ; killall python"
