# Setup



1. cd to the home directory

   `cd`
   

0. clone this repo

    `git clone git@github.com:alta3/ssh-githugger.git`
    

0. cd into the cloned directory

    `cd ssh-githugger/`
  
0. Run the setup script to load requirements plus python 3.8

    `./setup.sh`
  
0. Run the help example

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


### TODO

- [ ] Add more docstrings
- [ ] Cleanup functions, refactor if defaults are never exposed
- [ ] Add logging of all actions completed or failed (stderr) 
- [ ] Add last updated date to the serilization header comment
- [ ] Document how-to: Install in a venv
- [ ] Document how-to: Do a non-destructive test run (example usage)
- [ ] Document how-to: Deployment via systemd periodic task
- [ ] Document how-to: Deployment via cron job
- [ ] Document how-to: Install via ansible role
- [ ] Document how-to: Install via pip

### Possible future features

These didn't meet my imediate design goals but would not be difficult to add:

- Preserve current content of authorized_keys file
- Target remote systems (emulate `ssh-copy-id` functionality or wrap it)
