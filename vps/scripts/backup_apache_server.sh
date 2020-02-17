# Backup apache web server (/var/www/html/ directory)
echo /var/www/html/
datestamp=$(date "+%Y-%m-%d")
filename=${datestamp}.apache_server_backup.tar.gz
tar czf ~/backups/$filename /var/www/html/
