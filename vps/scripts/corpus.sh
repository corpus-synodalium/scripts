rm -rf ~/_output/*
unzip ~/output.zip
philoload4 -l ~/scripts/vps/config/custom_load_config.py corpus ~/_output/*.xml
cp -f ~/scripts/vps/config/web_config.cfg /var/www/html/philologic/corpus/data/web_config.cfg
cp ~/scripts/vps/config/logins.txt /var/www/html/philologic/corpus/data/
echo "Don't forget to run fixpermission corpus"
