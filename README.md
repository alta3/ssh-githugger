# Setup



1. cd to the home directory

   `cd`
   
0. Install git

    `sudo apt install -y git python3.8 virtualenv`
   
0. clone this repo, yes at the the prompt

    `git clone git@github.com:alta3/ssh-githugger.git`

0. cd into the cloned directory

    `cd ssh-githugger/`

0. Upgrade pip
    
    `sudo -H pip3 install --upgrade pip`

0. Install a 3.8 virtual environment.

    `python3.8 -m pip install virtualenv`
    
0. Create a 3.8 virtual environment

    `virtualenv -p python3.8 venv`
    
0. Activate the virtual enironment

    `source venv/bin/activate`

0. Run the setup script (again) inside the venv to load requirements 

    `./setup.sh`
  
0. Run the help example to determine if installation was successful.

    `python3.8 ssh-copy-id-from-github.py -h`
  
    ```
    usage: ssh-copy-id-from-github.py [-h] [-a] [-O | -f FILE] [-u USER] username [username ...]

    positional arguments:
      username              Public key source Github usernames

    optional arguments:
      -h, --help            show this help message and exit
      -a, --annotate        store public key source details in key annotation
      -O, --to-stdout       write results to standard output
      -f FILE, --file FILE  store output in FILE
      -u USE
      R, --user USER  store output for USER
    ```
  
0. Install the keys for Sam, Stu, Sean, and BJ. Please use the `-a` to add information about who owns the keys

    `python3.8 ssh-copy-id-from-github.py -a -f ~/.ssh/authorized_keys sfeeser seaneon bryfry sgriffith3`  

0. SHORTCUT!  Just run `sh ./get-keys.sh` to run the above command

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

    `sudo chmod 640 10-help-text 640 91-release-upgrade 50-motd-news`  

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




### TODO

- [ ] Add more docstrings
- [ ] Cleanup functions, refactor if defaults are never exposed
- [ ] Add logging of all actions completed or failed (stderr) 
- [ ] Add last updated date to the serilization header comment 
- [x] Document how-to: Install in a venv
- [ ] Document how-to: Do a non-destructive test run (example usage)
- [x] Document how-to: Deployment via systemd periodic task
- [ ] Document how-to: Install via ansible role
- [ ] Document how-to: Install via pip

### Possible future features

These didn't meet my imediate design goals but would not be difficult to add:

- Preserve current content of authorized_keys file
- Target remote systems (emulate `ssh-copy-id` functionality or wrap it)
