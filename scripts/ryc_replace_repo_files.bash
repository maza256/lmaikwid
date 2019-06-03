#!/bin/bash
###
#
# ryc_replace_repo_files.bash: update from the SourceForge repository on the Rolls-Royce Race Your Code laptops.
#
# 2019-03-26
#
###

# Get PiBorg code, after saving the opencv build files elsewhere.
cd ~
mv ~/RaceYourCodeVIRTUAL/opencvbuild ~/
sudo rm -r ~/RaceYourCodeVIRTUAL
git clone https://git.code.sf.net/p/rr-rycv/code ~/RaceYourCodeVIRTUAL
mv ~/opencvbuild ~/RaceYourCodeVIRTUAL/

# Sort out the files
ryc_USERNAME=`whoami`
read -p "Enter FTP password for $ryc_USERNAME: " ryc_FTPPASSWORD

sed -i.bak s/rycFTPPASSWORD/$ryc_FTPPASSWORD/g ~/RaceYourCodeVIRTUAL/scripts/ftp_upload.sh
sed -i.bak s/rycUSERNAME/$ryc_USERNAME/g ~/RaceYourCodeVIRTUAL/assets/Desktop/*.desktop
sed -i.bak s/rycUSERNAME/$ryc_USERNAME/g ~/RaceYourCodeVIRTUAL/scripts/*.sh

rm -r ~/Desktop/
rm ~/RaceYourCodeVIRTUAL/assets/Desktop/*.desktop.bak
mv ~/RaceYourCodeVIRTUAL/assets/Desktop ~/
echo "Organised files."

echo "Please edit the desktop shortcuts (but don't actually make changes). This is required to make the desktop icons executable."
# Now edit each desktop shortcut with gnome-desktop-item-edit to make them able to run
gnome-desktop-item-edit ~/Desktop/*.desktop
