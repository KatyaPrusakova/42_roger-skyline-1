<h1 align="center">
Roger-skyline-1
</h1>
<h1 align="center">
Initiation project to system and network administration.
</h1>

## Installation

##### Downloading and installing steps:

* **[Download](https://github.com/KatyaPrusakova/42_roger-skyline-1/archive/master.zip)**the latest version of the config.

# Command to check space and partion

`df -H`

# su -
# Command to add new user

`sudo adduser new_eprusako`
`sudo usermod -aG sudo new_eprusako`

# **Change user rights**

	`vim /etc/sudoers`
	`chmod 755 /etc/sudoers`
##################################################################################
	# User priviliege
	new_eprusako ALL=(ALL:ALL) ALL
	# Allow members of group sudo to execute any command
	%sudo   ALL=(ALL:ALL)   ALL
	new_eprusako ALL=(ALL:ALL)   NOPASSWD:ALL
##################################################################################

# Command to check static IP
# 255.255.255.252 corresponds to a /30 netmask.

	# 1) First step (change file to look like shown below)

 		`sudo vim /etc/network/interfaces`
##################################################################################
		 The primary network interface
		 auto enp0s3
##################################################################################
	# 2) Second step (create file to look like shown below)

		`sudo touch /etc/network/interfaces.d/enp0s3`
		`sudo vim /etc/network/interfaces.d/enp0s3`
##################################################################################
		iface enp0s3 inet static
			address 10.11.200.233
			netmask 255.255.255.252
			gateway 10.11.254.254
##################################################################################
		`sudo systemctl restart networking` or `sudo service networking restart`

# Setting up the SSH connection
# Comand to check status: sudo systemctl status ssh
	# 0) Open

		`sudo vim /etc/ssh/sshd_config`

	# 1)Uncomment fields below
##################################################################################
		Port 2222
		PermitRootLogin no
		PasswordAuthentification yes
##################################################################################
	# 2) Run on host computer

		`ssh-keygen -t ed25519 -C "My key for Debian"`
		`ssh-copy-id -i $HOME/.ssh/id_ed25519.pub new_eprusako@10.11.200.233 -p 2222`
		the key has been added so now its possible to log in

	# 3) Open

		sudo vim /etc/ssh/sshd_config

	# 4)Change field below

		PasswordAuthentification no

	# 5) Run

		sudo service sshd restart

	# 6) To test create new user and try to connect

		sudo adduser new_eprusako
		sudo adduser new_eprusako sudo

	# 7) Host computer

		ssh new_eprusako@10.11.200.233 -p 2222

# FIREWALL (iptable) better run on derbian if run
