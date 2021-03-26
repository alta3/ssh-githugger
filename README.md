# Setup


1. Clone githugger

   `git clone git@github.com:alta3/ssh-githugger`

0. cd

   `cd ssh-githugger`

0. Run the install script

   `bash setup.sh`

0. Run the help example to determine if installation was successful.

    `python3.8 ssh-copy-id-from-github.py -h`
 
0. Run with CLI (You should see a limit of 60)

   `python3 ssh-githugger.py sfeeser seaneon bryfry sgriffith3 -v` 

0. Follow these instructions to generate a personal auth token on GitHub 

   https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

0. export that token you just created (xxxxx below)

   `export GITHUB_OAUTH_TOKEN=xxxxxxxxxxxxxxxxxxx`

0. Run with CLI. (You should see LIMIT AS 5000)

   `python3 ssh-githugger.py sfeeser seaneon bryfry sgriffith3 -v

## Want to test this as a hello-world systemd service?

 > The following is a hardcoded hello-world example for a future ansible template.

0. On a VM that you do NOT mind deleting, run the hello world example (You will have to delete this service yourself if you do not choose a disposable VM)

0. Run the install script

   `bash setup.sh`

0. Now install the service

   `bash hello-world-setup.sh`

0. export that token you just created above (xxxxx below)

   `export GITHUB_OAUTH_TOKEN=xxxxxxxxxxxxxxxxxxx`

0. Restart the timer and the service. 

   `sudo systemctl restart ssh-githugger.timer && sudo systemctl restart ssh-githugger.service`

0. Check on your systemd timer. Make sure it is all green and running well. 

   `sudo systemctl status ssh-githugger.timer`

0. Check on your systemd service. Make sure it is all green and running well. 

   `sudo systemctl status ssh-githugger.service`

0. Now write the above as an asible template, or checkout the galaxy githugger role.

0. Run the help example to determine if installation was successful.

0. Display the changes to the .ssh authorized key file.

    `cat ~/.ssh/authorized_keys`

0. Exit the virtual environment like this

    `deactivate`

    ```
    (venv) ubuntu@sumi-09:~/ssh-githugger$ deactivate
    ubuntu@sumi-09:~/ssh-githugger$
    ```

### Create a service unit file for githugger.

1. Create a one-shot service unit file

    `sudo vim /etc/systemd/system/githugger.service`

   ```
   # Simple service unit file to run githugger as a one-shot
   #

   [Unit]
   Description=githugger ssh key updates
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=oneshot
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ssh-githugger/
   ExecStart=/home/ubuntu/ssh-githugger/venv/bin/python3.8 ssh-copy-id-from-github.py -a -f /home/ubuntu/.ssh/authorized_keys sfeeser seaneon bryfry sgriffith3
   StandardOutput=journal+console

   [Install]
   WantedBy=multi-user.target    
   ```
   
0. Create githugger timer 

    `sudo vim /etc/systemd/system/githugger.timer`

   ```
   [Unit]
   Description=Run ssh-githugger every day at 23:00 ZULU
   Requires=githugger.service

   [Timer]
   Unit=githugger.service
   OnCalendar=*-*-* 23:00:00
   RandomizeDelaySec=60
   AccuracySec=1s

   [Install]
   WantedBy=timers.target
   ```
   
0. This file does not need to be executable, but for security, it does need user and group ownership by root and 644 or 640 permissions

    `sudo chmod 644 /etc/systemd/system/githugger.service`

0. reload the daemon

    `sudo systemctl daemon-reload`

0. enable the service on boot.

    `sudo systemctl enable /etc/systemd/system/githugger.*`

0. start up the service

    `sudo systemctl start githugger.service`

0. start up the timer

    `sudo systemctl start githugger.timer`
    
### If you got this far, it is safe to remove SSH PASSWORDS!

1. Edit the ssh config file

    `sudo vim /etc/ssh/sshd_config`
    
     Set `PasswordAuthentication no`

0. Restart ssh server

    `sudo systemctl reload ssh`

### Create an informational welcome banner

1. Install landscape common to show status at login

    `sudo apt install landscape-common figlet -y`

0. Remove boring stuff from motd banner

    `cd /etc/update-motd.d`
    
    `sudo chmod 640 10-help-text 91-release-upgrade 50-motd-news`  

0. Add yellow figlet banner. Be sure to edit the sumi number

    `sudo vim /etc/update-motd.d/00-header`

    ```
    GREEN="\e[92m"
    YELLOW="\e[33m"
    WHITE="\e[37m"
    printf "${YELLOW}"
    figlet SUMI-xx  <--edit sumi number
    echo Keeper of VMs
    printf "${GREEN}"
    ```

### Possible future features

These didn't meet my imediate design goals but would not be difficult to add:

- Preserve current content of authorized_keys file
- Target remote systems (emulate `ssh-copy-id` functionality or wrap it)
