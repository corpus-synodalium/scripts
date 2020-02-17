# Backup /etc/apache2  and  /etc/philologic folders
echo /etc/apache2
echo /etc/philologic
datestamp=$(date "+%Y-%m-%d")
filename=${datestamp}.vps_etc_backup.tar.gz
tar czf ~/backups/$filename /etc/apache2/  /etc/philologic
