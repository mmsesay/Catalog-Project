# Catalog-Project
This is an item catalog project. A registered user can create a category and add items with description that belong to a specific category.
If a user is not registered they will only see the categories and navigate to it items but cannot perform some CRUD operations on them.
This project was written in python, SQLITE as database engine, Sqlalchemy as the ORM and it has implementation of OAuth Technology.

## Prerequisites
Below are the tools you need to have in order to execute this program:
1. Python:
- Installation for windows
    - Download the Python 3 Installer
    - Open a browser window and navigate to https://www.python.org/downloads/windows/ or at https://www.python.org/.
    - Underneath the heading at the top that says Python Releases for Windows, click on the link for the Latest Python 3 Release - Python 3.x.x. (As of this writing, the latest is Python 3.6.5.)
    - Scroll to the bottom and select either Windows x86-64 executable installer for 64-bit or Windows x86 executable installer for 32-bit. (See below.)
    - run the installer

- Installation for Python
    There is a very good chance your Linux distribution has Python installed already, but it probably won’t be the latest version, and it may be Python 2 instead of Python 3.
    - To find out what version(s) you have, open a terminal window and try the following commands:
        ```python --version```
        ```python2 --version```
        ```python3 --version```

    - If no python version dispaly, open your terminal ```CTRL + ALT + T``` and type the following commands:
    ```sudo add-apt-repository ppa:jonathonf/python-3.7```
    ```sudo apt-get update```
    ```sudo apt-get install python3.7```

- Installation for macOS / Mac OS X
    - Well the current versions of macOS include a version of Python 2 but still follow the process to install the python 3.
    - Open a browser and navigate to http://brew.sh/. After the page has finished loading, select the Homebrew bootstrap code under “Install Homebrew”. Then hit Cmd+C to copy it to the clipboard. Make sure you’ve captured the text of the complete command because otherwise the installation will fail.
    - Now you need to open a Terminal.app window, paste the Homebrew bootstrap code, and then hit Enter. This will begin the Homebrew installation.
    - If you’re doing this on a fresh install of macOS, you may get a pop up alert asking you to install Apple’s “command line developer tools”. You’ll need those to continue with the installation, so please confirm the dialog box by clicking on “Install”.
    - Confirm the “The software was installed” dialog from the developer tools installer.
    - Back in the terminal, hit Enter to continue with the Homebrew installation.
    - Homebrew asks you to enter your password so it can finalize the installation. Enter your user account password and hit Enter to continue.
    - Depending on your internet connection, Homebrew will take a few minutes to download its required files. Once the installation is complete, you’ll end up back at the command prompt in your terminal window.
    - Once Homebrew has finished installing, return to your terminal and run the following command:
    ```$ brew install python3```

2. Virtual Machine
    - Installation
    - Goto this https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 for your OS
    - Install the progam

3. Vagrant
    - Installation
    - Goto this link https://www.vagrantup.com/downloads.html to dowload the setup for your OS
    - Run the installer and verify if complete by typing : **vagrant --version**
    - Download the configuration file https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
    - Unzip the file. You will see a folder called FSND-Virtual-Machine. It may be located inside your Downloads folder.
    - change directory to FSND-Virtual-Machine. Inside, you will find another directory called vagrant.
    - run **vargran up** to start the vm
    - secondly run **vagrant ssh** to log into the vm-machine
    - Inside the vm change to the vagrant directory, **cd /vagrant**

4. **flask** : You need to create a virtual environment before install flask.
    The recommended way to create a virtual environment is to use the venv module. To install the python3-venv package that provides the venv module run the following command: ```sudo apt install python3-venv```
    1. Create a virtual environment directory: ```mkdir my_flask_app```
    2. Navigate to the virtual environment directory: ```cd my_flask_app```
    3. Once inside the directory, run the following command to create your new virtual environment: ```python3 -m venv venv```
    4. To start using this virtual environment, you need to activate it by running the activate script: ```source venv/bin/activate```
    5. Now that the virtual environment is activated, you can use the Python package manager pip to install Flask: ```(venv) pip install Flask```
    6. Verify the installation completed successfully with the following command which will print the Flask version: ```python -m flask --version```
    7. Now navigate back to the vagrant directory and clone the repo:
        ```git clone https://github.com/mmsesay/Catalog-Project.git```
    8. cd to the **Catalog-Project** directory

5. Install the following dependencies also:
    1. **sqlalchemy** : run the command: ```sudo easy_install sqlalchemy```
    2. **flask-login** : run the command: ```pip install flask-login```
    3. **oauth2client** : visit-> https://oauth2client.readthedocs.io/en/latest/ or type: ```pip install --upgrade oauth2client```
    4. **httplib2** : run the command: ```pip install httplib2```
    5. **requests** : run the command: ```pip install requests``` or ```easy_install requests```
    6. **werkzeug**: run the command: ```pip install Werkzeug``` or ```easy_install Werkzeug```
    7. **blinker**: Blinker provides a fast dispatching system that allows any number of interested parties to subscribe to events, or “signals”. run ```pip install blinker``` read more https://pypi.org/project/blinker/


## Executing the program
Make sure you are in the Catalog-Project directory, type: ``` python app.py ``` and hit enter

## How to use the API Endpoints
This program is running on localhost port 5000. Therefore, use the API endpoints like so http://localhost:5000/catalog/categories/JSON 

1. **/catalog/categories/JSON** : can return all the categories in the db
2. **/catalog/items/JSON** : can return all the items in the db
3. **/catalog/categoryName/JSON** - can return a specific category and it items. Eg **/catalog/Computer/JSON**
4. **/catalog/categoryName/itemName/JSON** - can return a specific category and a specific item that belong to it. Eg **/catalog/Computer/Mouse/JSON**
