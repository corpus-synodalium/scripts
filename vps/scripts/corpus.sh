# README
#
# What does this script do?
# - This script loads the XML files processed by the Python script
# (see https://github.com/corpus-synodalium/scripts/tree/master/xml)
# into the PhiloLogic database.
# - This will result in the following website being updated:
#   https://corpus-synodalium.com/philologic/corpus/
#
# Requirements
# - Create an empty "_output" folder at home (~) directory.
# - Copy the output.zip file to ~ folder. (You should have this file after running the Python script)
#
# Instructions
# - Run the following commands:
#     cd vps/scripts
#     source corpus.sh

# Clean _output folder
rm -rf ~/_output/*

# Unzip the XML files from output.zip into "~/_output" folder
unzip ~/output.zip -d ~

# Runs the "philoload4" command to load the database
# See https://github.com/corpus-synodalium/philo4-source/blob/master/docs/database_loading.md
# -l flag refers to LOAD_CONFIG file location
# "corpus" refers to the database name. This results in https://corpus-synodalium.com/philologic/corpus/
# "~/_output/*.xml" refers to the path of files to load
philoload4 -l ~/scripts/vps/config/custom_load_config.py corpus ~/_output/*.xml

# Copy the web_confing.cfg file to the correct folder. Notice the "corpus" folder
# Notice that we might have multiple instances of the database. e.g. We have
# - https://corpus-synodalium.com/philologic/corpus/
# - https://corpus-synodalium.com/philologic/corpusnorm/
# - https://corpus-synodalium.com/philologic/beta/
cp -f ~/scripts/vps/config/web_config.cfg /var/www/html/philologic/corpus/data/web_config.cfg

# The command below is commented out because we no longer restrict access to the database
# If you want to restrict aceess, you can define username and password in "logins.txt" file
# in tab-separted format e.g. "username<tab>mypassword"
# See https://github.com/corpus-synodalium/philo4-source/blob/master/docs/access_control.md
# cp ~/scripts/vps/config/logins.txt /var/www/html/philologic/corpus/data/

# Prints a reminder to run "fixpermission corpus"
# "fixpermission" is a bash command defined in .bashrc to update the permissions of the folders.
# If you don't run this, the website is inaccessible due to file permission issues.
#
#    function fixpermission() {
#    	chmod +x /var/www/html/philologic/$1/*.py;
#    	chmod +x /var/www/html/philologic/$1/reports/*.py;
#    	chmod +x /var/www/html/philologic/$1/scripts/*.py;
#    }
# If you don't have the "fixpermission" function defined, you can also run
# the three "chmod" commands above manually.
echo "Don't forget to run fixpermission corpus"
