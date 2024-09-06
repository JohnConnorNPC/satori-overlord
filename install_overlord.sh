
apt-get update
apt install dos2unix libunwind8 libglib2.0-0 ca-certificates -y

#Install Cron Job
cron_job="@reboot /overlord/overlord.sh"
crontab -l > /tmp/current_cron
grep -qxF "$cron_job" /tmp/current_cron || echo "$cron_job" >> /tmp/current_cron
crontab -u root /tmp/current_cron
rm /tmp/current_cron
reboot
