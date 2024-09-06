#!/bin/bash

cd /home/##username##
rm satori_cron_install_script.sh
wget -P /home/##username##/ ##server_url##/files/satori_cron_install_script.sh
dos2unix satori_cron_install_script.sh
chown daniel:daniel satori_cron_install_script.sh
chmod +x satori_cron_install_script.sh

# Add the cron job to run once

(crontab -u ##username## -l ; echo "@reboot /home/##username##/satori_cron_install_script.sh") | crontab -u ##username## -
sudo shutdown -r +1 "Rebooting in 1 minute..."