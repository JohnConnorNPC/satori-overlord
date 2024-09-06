
apt-get update
apt-get install python3-requests python3-psutil sudo dos2unix screen curl btop wget -y


#set no password on sudo
USERNAME="##username##"
usermod -aG sudo $USERNAME
SUDOERS_LINE="$USERNAME ALL=(ALL) NOPASSWD: ALL"
cp /etc/sudoers /etc/sudoers.bak

# Check if the line already exists to avoid duplication
if grep -q "^$SUDOERS_LINE" /etc/sudoers; then
    echo "The sudoers file already contains the NOPASSWD entry for $USERNAME."
else
    # If the line doesn't exist, add it to the sudoers file
    echo "$SUDOERS_LINE" | tee -a /etc/sudoers > /dev/null
    if [ $? -eq 0 ]; then
        echo "Successfully added NOPASSWD entry for $USERNAME to the sudoers file."
    else
        echo "Failed to add NOPASSWD entry to the sudoers file. Please check permissions."
    fi
fi

mkdir /minion
#get minion

curl -o /minion/minion.py ##server_url##/files/minion.py
curl -o /minion/minion.sh ##server_url##/files/minion.sh
chmod +x /minion/minion.sh
dos2unix /minion/minion.py
dos2unix /minion/minion.sh

#Install Cron Job
cron_job="@reboot /minion/minion.sh"
crontab -l > /tmp/current_cron
grep -qxF "$cron_job" /tmp/current_cron || echo "$cron_job" >> /tmp/current_cron
crontab -u root /tmp/current_cron
rm /tmp/current_cron
reboot
#screen -dmS session_name /minion/minion.sh
#btop
