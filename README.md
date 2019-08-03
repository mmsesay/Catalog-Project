# Catalog-Project
This is an item catalog project. A registered user can create a category and add items with description that belong to a specific category.
If a user is not registered they will only see the categories and navigate to it items but cannot perform some CRUD operations on them.
This project was written in python, SQLITE as database engine, Sqlalchemy as the ORM and it has implementation of OAuth Technology.

## Prerequisites
Below are the tools you need to have in order to execute this program:
1. Python:
..*Installation for windows
...Download the Python 3 Installer
...Open a browser window and navigate to https://www.python.org/downloads/windows/ or at https://www.python.org/.
...Underneath the heading at the top that says Python Releases for Windows, click on the link for the Latest Python 3 Release - Python 3.x.x. (As of this writing, the latest is Python 3.6.5.)
...Scroll to the bottom and select either Windows x86-64 executable installer for 64-bit or Windows x86 executable installer for 32-bit. (See below.)
...run the installer

..*Installation for windows
...There is a very good chance your Linux distribution has Python installed already, but it probably won’t be the latest version, and it may be Python 2 instead of Python 3.

...To find out what version(s) you have, open a terminal window and try the following commands:
...*python --version
...*python2 --version
...*python3 --version

...If no python version dispalys then run the following commands:
...*open your terminal CTRL + ALT + T
...*sudo add-apt-repository ppa:jonathonf/python-3.7
...*sudo apt-get update
...*sudo apt-get install python3.7

..*macOS / Mac OS X
...Well the current versions of macOS include a version of Python 2 but still follow the process to install the python 3.
...Open a browser and navigate to http://brew.sh/. After the page has finished loading, select the Homebrew bootstrap code under “Install Homebrew”. Then hit Cmd+C to copy it to the clipboard. Make sure you’ve captured the text of the complete command because otherwise the installation will fail.
...Now you need to open a Terminal.app window, paste the Homebrew bootstrap code, and then hit Enter. This will begin the Homebrew installation.
...If you’re doing this on a fresh install of macOS, you may get a pop up alert asking you to install Apple’s “command line developer tools”. You’ll need those to continue with the installation, so please confirm the dialog box by clicking on “Install”.
...Confirm the “The software was installed” dialog from the developer tools installer.
...Back in the terminal, hit Enter to continue with the Homebrew installation.
...Homebrew asks you to enter your password so it can finalize the installation. Enter your user account password and hit Enter to continue.
...Depending on your internet connection, Homebrew will take a few minutes to download its required files. Once the installation is complete, you’ll end up back at the command prompt in your terminal window.
...Once Homebrew has finished installing, return to your terminal and run the following command:

....$ brew install python3

2. Virtual Machine
..*Installation
...Goto this https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 for your OS
...Install the progam

3. Vagrant
..*Installation
...Goto this link https://www.vagrantup.com/downloads.html to dowload the setup for your OS
...Run the installer and verify if complete by typing : **vagrant --version**
...Download the configuration file https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
...Unzip the file. You will see a folder called FSND-Virtual-Machine. It may be located inside your Downloads folder.
...change directory to FSND-Virtual-Machine. Inside, you will find another directory called vagrant.
...run **vargran up** to start the vm
...secondly run **vagrant ssh** to log into the vm-machine
...Inside the vm change to the vagrant directory, **cd /vagrant**

4. Install this dependency in the vagrant directory

**flask** : you need to create a virtual environment before install flask.
    The recommended way to create a virtual environment is to use the venv module. To install the python3-venv package that provides the venv module run the following command: ```sudo apt install python3-venv```
    ...create a virtual environment directory and navigate to it
    ```mkdir my_flask_app```
    ```cd my_flask_app```
    ...Once inside the directory, run the following command to create your new virtual environment: ```python3 -m venv venv```
    ...To start using this virtual environment, you need to activate it by running the activate script: ```source venv/bin/activate```
    ...Now that the virtual environment is activated, you can use the Python package manager pip to install Flask:
    ```(venv) pip install Flask```
    ...Verify the installation was complete with the following command which will print the Flask version: ```python -m flask --version```
    ...now navigate back to the vagrant directory and clone the repo
    ```git clone https://github.com/mmsesay/Catalog-Project.git```
    ...cd to the **Catalog-Project** directory

5. Install the following dependencies also
    5.1. **sqlalchemy** : run the command ```sudo easy_install sqlalchemy```
    5.2. **flask-login** : run the command ```pip install flask-login```
    5.3. **oauth2client** : visit-> https://oauth2client.readthedocs.io/en/latest/ or type: ```pip install --upgrade oauth2client```
    5.4. **httplib2** : run the command ```pip install httplib2```
    5.5. **requests** : run the command ```pip install requests``` or ```easy_install requests```

6. Executing the program
...Make sure your in the Catalog-Project directory 
...type ``` python app.py ```

7. How to use the API Endpoints
...**/catalog/categories/JSON** : can return all the categories in the db
...**/catalog/items/JSON** : can return all the items in the db
...**/catalog/<categoryName>/JSON** - can return a specific category and it items. Eg **/catalog/Computer/JSON**
...**/catalog/<categoryName>/<itemName>/JSON** - can return a specific category and a specific item. Eg **/catalog/Computer/Mouse/JSON**
