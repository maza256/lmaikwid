#!/bin/bash

# FTP settings
HOST="217.36.211.159"
USER="fpi_rycUSERNAME"
PASS="rycFTPPASSWORD"

echo "Backing up previous local tarball..."
# Backup the previous local version
cd ~/RaceYourCodeVIRTUAL/code/
rm RYCV_code.tar.gz~
mv RYCV_code.tar.gz RYCV_code.tar.gz~

echo "Compressing current code into a tarball..."
# Compress the folder, ignoring some files
tar -czvf formulapi.tar.gz -X tar.exclude *

echo -e "Will now attempt to upload via FTP. \nOnce uploaded, the remote server will list the files. \nThere should be at least the two files:\n\tformulapi.tar.gz \n\tformulapi.tar.gz~\nIf formulapi.tar.gz tarball does not exist, the upload was not successful."
# Upload the new version to the FTP
ftp -n -v $HOST <<END_FTP
user $USER $PASS
binary
delete formulapi.tar.gz~
rename formulapi.tar.gz formulapi.tar.gz~
put formulapi.tar.gz
ls
quit
END_FTP

echo "Finished with FTP."

read -p "Press enter to close terminal: " response

mv formulapi.tar.gz RYCV_code.tar.gz
