# Item Catalog Project #

## 1. Program Description ##

This program is python based web application for an **Item Catalog**.

The web application allows users to view items in a variety of pre-defined categories. Authenticated users are also able to create, edit and delete items.

## 2. Installation Requirements ##

### 2.1 Program Environment ###

This program was created and tested using the following environment:  
  
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads "Virtualbox Download") (Virtualization Software)  
- [Vagrant](https://www.vagrantup.com/ "Vagrant Download") (VM Provisioning and configuration)  
- Udacity Project VM Configuration Files (Available via [Direct Download](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) or [Github Repo](https://github.com/udacity/fullstack-nanodegree-vm))  
  - VM configuration includes the following used in this project:  
  - Ubuntu 16.04.5 LTS  
  - python 2.7.12  
  - psql 9.5.14

- Unix style terminal program (Default OS terminal on Mac/Linux, Recommend [Git Bash](https://git-scm.com/downloads) on Windows)

- Web Browser

### 2.2 Program Files ###

In order to run this program these files and folders should be in the working directory:  
  
- application.py
- category_setup.py
- client_secrets.json
- database_setup.py
- itemcatalog.db
- README.md
- static/
    - styles.css
- templates/
    - catalog.html
    - deleteItem.html
    - editItem.html
    - header.html
    - itemDesc.html
    - itemList.html
    - login.html
    - main.html
    - newItem.html
    - publicCatalog.html
    - publicHeader.html
    - publicItemDesc.html

### 2.3 Setup ###

In order to setup and prepare the environment to run this program - follow these basic steps:

1. Download and install VirtualBox *(Consult VirtualBox documentation for more detailed instructions)*
2. Download and install Vagrant *(Consult Vagrant documentation for more detailed instructions)*
3. Download the VM Configuration files, extract if needed, and save to your desired directory
4. Place the Program Files (outlined in section 2.2 above) in the /vagrant directory of the VM configuration folder
5. Navigate to the /vagrant directory using your terminal program and provision the VM using the command int the terminal: `vagrant up`  
6. **Note:** The initial setup may take a while as the appropriate files are downloaded and installed.  Subsequent startups will be much faster after this inital configuration.
7. Log into the VM using the command in the terminal: `vagrant ssh`
8. You have now setup your environment and are ready to use the program!

## 3. Using the Program ##

### 3.1 Database & Server Setup

While logged into the VM, in the terminal, navigate to the directory with the program files and create the database for the program using the following command:  

`python database_setup.py`

Populate the database with the base categories and items by using the command:

`python category_setup.py`

Start the web server by running the command:  

`python application.py`  

### 3.2 Web Application

To use the web application, open your Web Browser and navigate to the address:

[http://localhost:8000](http://localhost:8000)

#### 3.2.1 Top Menu 
- Home: Return to the Catalog Home Page
- Login/Logout: Login or Logout using your Google Account (if you do not have an account you will need to create one to authenticate with this application)

#### 3.2.2 Main Page (`http://localhost:8000/catalog or http://localhost:8000`)
- Categories: Shows all the available pre defined categories. Selecting a category will bring up all of the available items in that category (See 3.2.3 Category Items).
- Latest Items: Shows the 9 most recently created items and their categories. Selecting an item will bring up the detail page for that item.
- Add Item (Authenticated Users Only): Brings up the page to create a new item.

#### 3.2.3 Category Items (`http://localhost:8000/catalog/<category_name>/items`)
- Categories: Shows all the available pre defined categories. Selecting a category will bring up all of the available items in that category (See 3.2.3 Category Items).
- (Category) Items: Shows all of the available items in the selected category. Selecting an item will bring up the detail page for that item.
- Add Item (Authenticated Users Only): Brings up the page to create a new item.

#### 3.2.4 Item Description (`http://localhost:8000/catalog/<category_name>/<item_name>`)
- This page shows the selected item name and description
- (Authenticated Users Only): Links to Edit or Delete allow authenticated users to edit or delete the described item.

#### 3.2.5 Add Item (`http://localhost:8000/catalog/items/new`)
- This page allows an authenticated user to create a new items by providing a name, description and category. Clicking Create creates the new item in the database.

#### 3.2.6 Edit Item (`http://localhost:8000/catalog/<item_name>/edit`)
- This page allows an authenticated user to edit the described item. Clicking Edit updates the item in the database.

#### 3.2.7 Delete Item (`http://localhost:8000/catalog/<category_name>/items`)
- This page allows an authenticated user to delete the described item. Clicking Delete deletes the item from the database. Clicking cancel will return the user to the home page without deleting the item. 

#### 3.2.8 JSON API
- This API allows a user with the API key to read details of the catalog in a JSON format. The user must append the Query Parameter: `?key=super_secret_key` to the desired API URI in order to view the JSON output. 

##### 3.2.8.1 JSON API - (`http://localhost:8000/api/v1/catalog)
- This endpoint outputs the content of the entire catalog in JSON.

##### 3.2.8.2 JSON API - (`http://localhost:8000/api/v1/catalog/<category_name>)
- This endpoint outputs the category and all of its items in a JSON format. If the category name contains spaces, they must be replaced in the URI as `%20`. 

##### 3.2.8.3 JSON API - (`http://localhost:8000/api/v1/catalog/<category_name>/<item_name>)
- This endpoint outputs the specified item in a JSON format. If the category or item names contains spaces, they must be replaced in the URI as `%20`. 

## 4. References
- Code snippets taken in part from Udacity Full Stack Web development nanodegree lessons
- Web application interface inspired by Udacity "Restaurant Menu" application