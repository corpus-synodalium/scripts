rm -rf ~/_output/*
unzip ~/output_norm.zip -d ~
philoload4 -l ~/scripts/vps/config/custom_load_config.py beta2 ~/_output/*.xml
cp -f ~/scripts/vps/config/web_config.cfg /var/www/html/philologic/beta2/data/web_config.cfg
# cp ~/scripts/vps/config/logins.txt /var/www/html/philologic/beta2/data/
echo "Don't forget to run fixpermission beta2"
