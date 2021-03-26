sudo apt install python3.8

python3.8 -m pip install -r requirements.txt

sudo cp ssh-githugger.service /etc/systemd/system/
sudo cp ssh-githugger.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start ssh-githugger.service
sudo systemctl enable ssh-githugger.service
sudo systemctl start ssh-githugger.timer
sudo systemctl enable ssh-githugger.timer

