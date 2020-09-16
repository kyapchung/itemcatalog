# Linux Server Configuration/Web Application Project

## Project Description

This project is simple custom "Item Catalog" web application running via the Web Server Gateway Interface (WSGI) scheme on an Ubuntu Linux server image. The Linux server has been configured according to the following documentation, as per the requirements of the Udacity Linux Server Configuration Project Specification.

The final application was* (*I no longer have this project actively hosted) hosted at: 
URL: [http://ec2-52-37-173-65.us-west-2.compute.amazonaws.com](http://ec2-52-37-173-65.us-west-2.compute.amazonaws.com/catalog)
Server IP: [http://52.37.173.65](http://52.37.173.65)

To SSH into the server, save the private key to the .ssh/ directory on the private terminal and run:
`ssh grader@52.37.173.65 -p 2200 -i ./.ssh/id_rsa.pem`

## Summary of Software installed:

- Server: Ubuntu 16.04.4 instance running via Amazon Lightsail [https://aws.amazon.com/lightsail/](https://aws.amazon.com/lightsail/)

- All system packages updated to the latest versions by running:

`sudo apt-get update`
`sudo apt-get upgrade`
`sudo apt-get dist-upgrade`

- Installed packages via apt-get:
    - apache2
    - libapache2-mod-wsgi 
    - python-dev
    - git
    - python-pip
    - postgresql

- Installed packages in venv/ via pip:
    - Flask
    - httplib2 
    - oauth2client
    - sqlalchemy
    - psycopg2
    - sqlalchemy_utils
    - requests

## Summary of Configurations

### Amazon Lightsail

- Connections allowed on:
    - HTTP TCP 80
    - NTP TCP 123
    - SSH TCP 2200

- Assigned a static IP address
- Using default account private key for remote SSH access

### Server Updates
- All packages updates to most recent versions via:
`sudo apt-get update`
`sudo apt-get upgrade`
`sudo apt-get dist-upgrade`

### SSH Configuration

Edit /etc/ssh/sshd_config to change SSH sonfiguration.

- Port changed from 22 to 2200:
    - Port 2200
- Disable root login
    - PermitRootLogin no
- Enforce key based authorization
    - PasswordAuthentication no

### UFW Firewall

- Allow all outgoing connections
- Incoming connections only allowed on:
    - SSH TCP 2200
    - HTTP TCP 80
    - NTP 123

### Users & Permissions
- Added users:
    - grader
    - itemcatalog
- Added sudo permissions for both users by modifying /etc/sudoers.d and adding files with lines:
    - grader ALL=(ALL:ALL) ALL
    - itemcatalog ALL=(ALL:ALL) ALL

### RSA Key Authentication

Created an RSA key pair for the grader account remote ssh login using:

`sudo ssh-keygen`

Save public key to grader home directory in:

./.ssh/authorized_keys

### Set local time to UTC

While logged in as grader run:

`sudo dpkg-reconfigure tzdata`

Set geographic area to "None" and timezone to UTC.

### Set up App Directory

Set up the app directory in /var/www/

`cd /var/www`
`sudo mkdir itemcatalog`

Import the WSGI project files from the git repository

`git clone https://github.com/kyapchung/itemcatalog.git itemcatalog` 

### Configure Apache for WSGI app

`sudo nano /etc/apache2/sites-available/itemcatalog.conf`

    <VirtualHost *:80>
        ServerName 52.37.173.65
        ServerAlias ec2-52-37-173-65.us-west-2.compute.amazonaws.com
        ServerAdmin admin@52.37.173.65
        WSGIDaemonProcess itemcatalog python-path=/var/www/itemcatalog:/var/www/itemcatalog/itemcatalog/venv/lib/python2.7/site-packages
        WSGIProcessGroup itemcatalog
        WSGIScriptAlias / /var/www/itemcatalog/itemcatalog.wsgi
        <Directory /var/www/itemcatalog/itemcatalog/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/itemcatalog/itemcatalog/static
        <Directory /var/www/itemcatalog/itemcatalog/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>`

### Configure Postgresql

Switch to the postgres user using:

`sudo su postgres`

Open PostgreSQL interactive terminal with:

`psql`

Create a `itemcatalog` user with a password and give them the ability to create databases:

`CREATE USER itemcatalog WITH PASSWORD 'udacity';`
`ALTER USER itemcatalog CREATEDB;`
`CREATE DATABASE itemcatalog WITH OWNER itemcatalog;`

Connect to database:

 `\c itemcatalog`

`REVOKE ALL ON SCHEMA public FROM public;`
`GRANT ALL ON SCHEMA public TO itemcatalog;`
`CREATE DATABASE catalog WITH OWNER itemcatalog;`

to list existing roles run:

`\du.`

Exit psql using:

`\q`

Switch back to the grader user: 

`exit`

Reset the apache server

`sudo service apache2 restart`

Enable the application

`sudo a2ensite itemcatalog`

## Appendix:

Useful command for troubleshooting Apache server errors:

`sudo tail /var/log/apache2/error.log`

## References:

- [Udacity Project Specification](https://review.udacity.com/#!/rubrics/2007/view)
- [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [https://github.com/juvers/Linux-Configuration](https://github.com/juvers/Linux-Configuration)
- [https://github.com/boisalai/udacity-linux-server-configuration](https://github.com/boisalai/udacity-linux-server-configuration)
