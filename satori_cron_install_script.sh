#!/bin/bash
sudo apt update && sudo apt install btop screen unzip -y && sudo apt upgrade -y


# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update


sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin unzip -y




cd ~
wget -P ~/ https://satorinet.io/static/download/linux/satori.zip
unzip ~/satori.zip
rm ~/satori.zip
cd ~/.satori
sudo apt-get install python3-venv -y
bash install.sh
bash install_service.sh &

sleep 30
bash install.sh
bash install_service.sh


crontab -u ##username## -l | grep -v '/home/##username##/satori_cron_install_script' | crontab -u ##username## -
sudo shutdown -r +1 "Rebooting in 1 minute..."
