<h1 align="center">
Roger-skyline-1
</h1>
<h1 align="center">
Initiation project to system and network administration.
</h1>


### V.1 VM Part

I used VirtualBox to install Debian 10.5.0 amd64 netinst.

* Following properties:

Disk size of 8 GB
Has a 4.2 GB partition

 * Software installed:

web server
print server
SSH server
standard system utilities

* Command to disk space and partion:

`df -h`

**Command to add new user**

	`sudo adduser new_eprusako`
	`sudo usermod -aG sudo new_eprusako`

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


# FIREWALL (iptable) better run on derbian if run



### VI.1 Web Part

Create a Self-Signed SSL Certificate using Apache in Debian



### VI.2 Deployment Part

## Deployment installation

##### Downloading and installing steps:

* [Download](https://github.com/KatyaPrusakova/42_roger-skyline-1/archive/master.zip) the latest version of the config.
* Run command in terminal `bash deployment_script.sh` in order
