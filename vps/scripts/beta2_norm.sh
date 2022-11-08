rm -rf ~/_output/*
unzip ~/output_norm.zip -d ~
philoload4 -l ~/scripts/vps/config/custom_load_config.py beta2 ~/_output/*.xml
cp -f ~/scripts/vps/config/web_config.cfg /var/www/html/philologic/beta2/data/web_config.cfg
# cp ~/scripts/vps/config/logins.txt /var/www/html/philologic/beta2/data/
echo "Don't forget to run fixpermission beta2"

# Need to manually update the page title in HTML file to have (Normalized)
# e.g. "Corpus Synodalium" => "Corpus Synodalium (Normalized)"
echo "Don't forget to update \"title\" \$DBNAME in HTML file to ... (Normalized)"
echo "vim /var/www/html/philologic/beta2/app/index.html"
