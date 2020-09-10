<h1 align="center">
Roger-skyline-1
</h1>
<h1 align="center">
Initiation project to system and network administration.
</h1>

<h1 align="center">
V.1 VM Part
</h1>

For this project I used VirtualBox in order to install Debian 10.5.0 amd64 netinst.

* Following properties:

	* Disk size of 8 GB
	* Has a 4.2 GB partition

 * Software installed:

	* web server
	* print server
	* SSH server
	* standard system utilities

* Command to check disk space and partion:

	`df -h`

**Command to add new user**

My new user will be called `new_eprusako`

	sudo adduser new_eprusako
	sudo usermod -aG sudo new_eprusako

 **Change user rights**

	vim /etc/sudoers
	chmod 755 /etc/sudoers

File `sudoers` should look like this:

	# User priviliege
	sudo			ALL=(ALL:ALL)		ALL
	new_eprusako		ALL=(ALL:ALL)		ALL

	# Allow members of group sudo to execute any command
	%sudo			ALL=(ALL:ALL)		ALL
	new_eprusako		ALL=(ALL:ALL)		NOPASSWD:ALL

 **Command to check static IP**

1. File `interfaces` should look like this:

	sudo vim /etc/network/interfaces

		The primary network interface
		auto enp0s3

2. Create file `enp0s3` with command `sudo vim /etc/network/interfaces.d/enp0s3`.

3. File `enp0s3` should look like this:

		iface enp0s3 inet static
			address 10.11.200.233
			netmask 255.255.255.252
			gateway 10.11.254.254

255.255.255.252 corresponds to a /30 netmask.

4. Run restart

`sudo systemctl restart networking` or `sudo service networking restart`

---

**Setting up the SSH connection**

---

Comand to check status: `sudo systemctl status ssh`

1. Open

	`sudo vim /etc/ssh/sshd_config`

2. Uncomment fields below

		Port 2222
		PermitRootLogin no
		PasswordAuthentification yes

3. Run on host computer

ssh-keygen -t ed25519 -C "My key for Debian"`
ssh-copy-id -i $HOME/.ssh/id_ed25519.pub new_eprusako@10.11.200.233 -p 2222

The key has been added to VM so now its possible to log in.

4. Open

sudo vim /etc/ssh/sshd_config

5. Change file

		PasswordAuthentification no

6. Run

	`sudo service sshd restart`

7. To test create new user and try to connect

	`sudo adduser new_eprusako`
	`sudo adduser new_eprusako sudo`

8. Host computer

	`ssh new_eprusako@10.11.200.233 -p 2222`

If you try to connect with different user it should show `Permission denied (publickey).` error. To see more details connect with `ssh -v`

---

**Firewall and DOS protection**

---

	echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
	echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections

	sudo apt-get -y install iptables-persistent

You can verify these fields by installing debconf-utils and searching for iptables values:

	sudo apt install debconf-utils

	sudo debconf-get-selections | grep iptables

	sudo ufw enable

	sudo ufw allow 2222
	sudo ufw allow 80/tcp
	sudo ufw allow 443/tcp
	sudo service ufw restart
	sudo ufw status numbered

HTTP on port 80, which is what unencrypted web servers use, using sudo ufw allow http or sudo ufw allow 80
HTTPS on port 443, which is what encrypted web servers use, using sudo ufw allow https or sudo ufw allow 443

	sudo systemctl status fail2ban.service

1. Add file

	sudo vim /etc/fail2ban/jail.d/jail-debian.local

		[sshd]
		port = ssh
		logpath = %(sshd_log)s
		backend = %(sshd_backend)s
		enabled = true
		filter  = sshd
		action  = iptables
		maxretry = 3
		findtime = 1d
		bantime = 2w

2. Restart

	sudo service fail2ban restart

If you try to connect via `ssh` with incorrect password, it will resulted IP ban. If you want to unban, run command:

	sudo fail2ban-client set sshd unbanip 10.11.200.233

If you want to delete run `sudo apt-get autoremove --purge fail2ban`

If you want to check ssh banned informtion run `journalctl -u ssh.service` and to checl all log info run  `ls -l /var/log/*.log`

---

**Port scanning**

---

If you want to test you port scanning run `scan.py` file from this repository. All hosts that have been benned are saved in the file `sudo vim /etc/hosts.deny`

1. Change file

	sudo vim /etc/default/portsentry

		TCP_MODE="atcp"
		UDP_MODE="audp"

2. Change file

	sudo vim /etc/portsentry/portsentry.conf

		# only one KILL shall be uncommented

		BLOCK_UDP="1"
		BLOCK_TCP="1"
		KILL_ROUTE="/sbin/iptables -I INPUT -s $TARGET$ -j DROP"

3. Check and restart

		sudo cat /etc/portsentry/portsentry.conf | grep KILL_ROUTE | grep -v "#"
		sudo /etc/init.d/portsentry start
		# in order to check: sudo cat /var/log/syslog

---

**Stop the services you don’t need for this project.**

---

Check running services:

`sudo ls /etc/init.d` or `sudo service --status-all`

Disable command:

	sudo systemctl disable console-setup.service
	sudo systemctl disable keyboard-setup.service
	sudo systemctl disable bluetooth.service

---

**Cron scripts**

---

1. Add script:

	sudo vim /root/scripts/update_script.sh

		#!/bin/bash
		apt update -y >> /var/log/update_script.log
		apt upgrade -y >> /var/log/update_script.log

2. Modify crontab `sudo VISUAL=vi crontab -e`

		`0 4 * * wed root /root/scripts/update_script.sh`
		`@reboot root /root/scripts/update_script.sh`

3. Create script to send email if crontab was modified `monitor_cron.sh`

		#!/bin/bash
		now="md5sum /etc/crontab"
		old="/home/katya/cron_tab_status"
		if [ "$now" != "$old" ]; then
			echo "Crontab has been modified" | mail -s "Crontab has been modified" root
		fi
		md5sum /etc/crontab > /home/katya/cron_tab_status

4. Check mail as root to see changes.




<h1 align="center">
VI.1 Web Part
</h1>

Create a Self-Signed SSL Certificate using Apache in Debian.

**Copy**

	sudo chmod 777 /var/www/html/index.html
	scp -P 2222 index.html  new_eprusako@10.11.200.233:/var/www/html/index.html

**Run command**

	sudo openssl req -x509 -nodes -days 365 -subj "/C=FI/ST=Helsinki/L=Helsinki/O=Global Security/OU=IT Department/CN=10.11.200.233/emailAddress=root@roger.lan" -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt

**Create file**

	sudo vim /etc/apache2/conf-available/ssl-params.conf

		SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
		SSLProtocol All -SSLv2 -SSLv3
		SSLHonorCipherOrder On

		Header always set X-Frame-Options DENY
		Header always set X-Content-Type-Options nosniff

		SSLCompression off
		SSLSessionTickets Off
		SSLUseStapling on
		SSLStaplingCache "shmcb:logs/stapling-cache(150000)"


**Make backup**

	sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf_backup

**Edit file**

	sudo vim /etc/apache2/sites-available/default-ssl.conf

		ServerAdmin root@roger
		ServerName 10.11.200.233
		DocumentRoot /var/www/html
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
		SSLEngine on
		SSLCertificateFile	#uncomment
		SSLCertificateKeyFile #uncomment

**Edit file**

	sudo vim /etc/apache2/apache2.conf

		ServerName 10.11.200.233

**Check and restart**

	sudo apache2ctl configtest
	sudo service apache2 restart

**Ad redirect**

	sudo vim /etc/apache2/sites-available/000-default.conf


Redirect "/" "https://10.11.200.233/"

	sudo a2enmod ssl
	sudo a2enmod headers
	sudo a2ensite default-ssl
	sudo a2enconf ssl-params
	sudo apache2ctl configtest
	sudo systemctl reload apache2


<h1 align="center">
VI.2 Deployment Part
</h1>


**Deployment installation**

##### Downloading and installing steps:

* [Download](https://github.com/KatyaPrusakova/42_roger-skyline-1/archive/master.zip) the latest version of the config.
* Run command in terminal `bash deployment_script.sh` in order to deploy.


