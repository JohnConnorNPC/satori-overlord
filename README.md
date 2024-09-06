# Satori Overlord

**Satori Overlord** is a server-client management platform designed to manage and monitor connected minions from a centralized GUI interface. The Overlord server controls, executes, and manages scripts on the connected minions, including installation, updates, and system maintenance tasks.  The server is written in Xojo and provides a web GUI.  You can compile Xojo linux applications for free on linux with a free license.  www.xojo.com.  The client is written in Python.



## Key Features
- **Centralized Management**: Manage multiple clients (minions) through a single server interface.
- **Script Execution**: Easily execute and update scripts on remote minions.
- **System Monitoring**: Monitor the status of each minion, check installation status, version numbers, and online status in real-time.
- **Customizable Replacements**: Configure text replacements for `.py` and `.sh` scripts directly through the settings page.
- **Contextual Right-Click Menus**: Utilize right-click options for host management, including rebooting, shutting down, restarting Satori, and opening Vault or Wallet.

---

## Manual

Written for debian based systems.  Tested on Debian 12.

### Settings

The settings page allows you to configure text replacements that are served in both `.py` and `.sh` files. These placeholders can be used to dynamically insert values such as usernames, server URLs, paths, passwords, and trigger times. The current available settings include:

- **##username##**: Set the username.
- **##server_url##**: Define the server URL.
- **##satori_path##**: Define the Satori path on the client machine.
- **##vault_password##**: Set the vault password.
- **##client_trigger##**: Define the trigger interval for the client.

Additionally, there's an option to simulate reboot and shutdown actions using the `-k` flag if required.

After making any changes to the settings, click `Save` to apply them.

### Main Interface

The main interface displays a list of connected minions along with their current status and other important information:

| **Field**         | **Description**                                                                 |
|-------------------|---------------------------------------------------------------------------------|
| **Host**          | Name of the client (minion) device.                                              |
| **Last Checkin**  | The last time the client checked in with the server.                             |
| **Satori Installed** | Indicates whether Satori is installed on the minion.                          |
| **Satori Online** | Shows if Satori is currently online.                                             |
| **$ Satori**      | Displays the balance                                                             |
| **Satori Version**| Shows the current version of Satori installed.                                   |
| **Pending Action**| Indicates if there are pending actions for the minion.                           |
| **Minion Version**| Displays the minion's version.                                                   |

### Right-Click Options

#### Hosts (Minions)
By right-clicking on any minion in the host list, you are presented with the following options:
- **Refresh**: Refresh the Listbox View.
- **Reboot**: Reboot the minion remotely.
- **Shutdown**: Shutdown the minion.
- **Delete**: Remove the minion from the list.
- **Restart Satori**: Restart the Satori service on the minion.
- **Open Vault**: Access the vault on the minion.
- **Open Wallet**: Access the wallet on the minion.

#### Scripts
The upload button lets you upload external scripts into the Overlord.
You can also right-click on any script in the scripts list for the following options:
- **Run**: Execute the selected script on the minion.
- **Edit**: Open and edit the script.  (previous file is archived to ./archive/ with a random guid at the end of the name).
- **Archive**: Archive the script (file is moved to ./archive/ with a random guid at the end of the name).
- **Hide/Unhide**: Toggle the visibility of the script in the list.

---

## Installation

### Server Setup
1. Download the release files and extract them to the `/overlord` directory on your server.
2. run: apt install dos2unix libunwind8 libglib2.0-0 ca-certificates
3. Add the `overlord.sh` script to the root cron for automatic startup:
    ```bash
    sudo crontab -e -u root
    ```
   Add the following line:
    ```bash
    @reboot /overlord/overlord.sh
    ```
4. Reboot the server and access the GUI via `http://server_ip_or_host:8080`.

### Client (Minion) Setup
1. Edit the `install_minion.sh` script from the GUI to suit your client setup.
2. On the client machine, open a terminal with root access and run the following:
    ```bash
    apt install curl -y
    curl -fsSL http://server_ip_or_host:8080/files/install_minion.sh | sh
    ```
This will install the minion and connect it to the Overlord server.

---

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License - see the [LICENSE](LICENSE.md) file for details.

Copyright (C) https://github.com/JohnConnorNPC
---

## Screenshots

![image](https://github.com/user-attachments/assets/27c04ce2-8c24-4121-8303-379ea29e2e8d)
![image](https://github.com/user-attachments/assets/768589c4-c7c2-420a-886c-cb08351e632a)
![image](https://github.com/user-attachments/assets/1d031791-8f45-48f3-ae76-9e3ebfb3a881)
![image](https://github.com/user-attachments/assets/6bfe1097-82c0-48c3-b9a2-4f2fc3c62c1e)

