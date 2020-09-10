<h1 align="center">
Roger-skyline-1
</h1>
<h1 align="center">
Initiation project to system and network administration.
</h1>


### V.1 VM Part

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

	sudo adduser new_eprusako
	sudo usermod -aG sudo new_eprusako

 **Change user rights**

	`vim /etc/sudoers`
	`chmod 755 /etc/sudoers`

File should look like this:

	# User priviliege
	sudo			ALL=(ALL:ALL)		ALL
	new_eprusako	ALL=(ALL:ALL)		ALL

	# Allow members of group sudo to execute any command
	%sudo			ALL=(ALL:ALL)		ALL
	new_eprusako	ALL=(ALL:ALL)		NOPASSWD:ALL


 **Command to check static IP**

255.255.255.252 corresponds to a /30 netmask.

1. First step (change file to look like shown below)

 	`sudo vim /etc/network/interfaces`

		 The primary network interface
		 auto enp0s3

2. Second step (create file to look like shown below)

	`sudo touch /etc/network/interfaces.d/enp0s3`
	`sudo vim /etc/network/interfaces.d/enp0s3`

		iface enp0s3 inet static
			address 10.11.200.233
			netmask 255.255.255.252
			gateway 10.11.254.254

`sudo systemctl restart networking` or `sudo service networking restart`

**Setting up the SSH connection**
Comand to check status: `sudo systemctl status ssh`

1. Open

	`sudo vim /etc/ssh/sshd_config`

2. Uncomment fields below

		Port 2222
		PermitRootLogin no
		PasswordAuthentification yes

3. Run on host computer

	`ssh-keygen -t ed25519 -C "My key for Debian"`
	`ssh-copy-id -i $HOME/.ssh/id_ed25519.pub new_eprusako@10.11.200.233 -p 2222`
the key has been added so now its possible to log in

4. Open

	sudo vim /etc/ssh/sshd_config

5. Change field below

		PasswordAuthentification no

6. Run

		sudo service sshd restart

7. To test create new user and try to connect

		sudo adduser new_eprusako
		sudo adduser new_eprusako sudo

8. Host computer

	ssh new_eprusako@10.11.200.233 -p 2222


# FIREWALL

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
	#HTTP on port 80, which is what unencrypted web servers use, using sudo ufw allow http or sudo ufw allow 80
	#HTTPS on port 443, which is what encrypted web servers use, using sudo ufw allow https or sudo ufw allow 443

##

	sudo systemctl status fail2ban.service

1. Change file

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


# Port scanning

after running scan.py

	sudo vim /etc/hosts.deny

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

# Stop the services you don’t need for this project.

	# Check running services
	sudo ls /etc/init.d
	# or sudo service --status-all

	sudo systemctl disable console-setup.service
	sudo systemctl disable keyboard-setup.service
	sudo systemctl disable bluetooth.service
	sudo systemctl disable syslog.service

	# sudo systemctl disable keyboard-setup.sh depending on donwloaded version


### VI.1 Web Part

Create a Self-Signed SSL Certificate using Apache in Debian

#Copy

	sudo chmod 777 /var/www/html/index.html
	scp -P 2222 index.html  new_eprusako@10.11.200.233:/var/www/html/index.html

#RUN COMMAND

	sudo openssl req -x509 -nodes -days 365 -subj "/C=FI/ST=Helsinki/L=Helsinki/O=Global Security/OU=IT Department/CN=10.11.200.233/emailAddress=root@roger.lan" -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt

#CREATE FILE

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


#MAKE BACKUP

	sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf_backup

#EDIT FILE

	sudo vim /etc/apache2/sites-available/default-ssl.conf

##################################################################################
		ServerAdmin root@roger
		ServerName 10.11.200.233
		DocumentRoot /var/www/html
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
		SSLEngine on
		SSLCertificateFile	#uncomment
		SSLCertificateKeyFile #uncomment
##################################################################################

# EDITFILE

	sudo vim /etc/apache2/apache2.conf

ServerName 10.11.200.233

# CHECK AND RESTART

	sudo apache2ctl configtest
	sudo service apache2 restart

# ADD REDIRECT

	sudo vim /etc/apache2/sites-available/000-default.conf


Redirect "/" "https://10.11.200.233/"

	sudo a2enmod ssl
	sudo a2enmod headers
	sudo a2ensite default-ssl
	sudo a2enconf ssl-params
	sudo apache2ctl configtest
	sudo systemctl reload apache2


### VI.2 Deployment Part

## Deployment installation

##### Downloading and installing steps:

* [Download](https://github.com/KatyaPrusakova/42_roger-skyline-1/archive/master.zip) the latest version of the config.
* Run command in terminal `bash deployment_script.sh` in order
