# **Bertram - The Managing Bot**
**readme in constant update, check frequently*


## **Bertram's Objectives**
The Bertram Bot idea was created in order to lighten the developer's work involving server version management, database access, and interaction and to reduce access to the server's machine.


This project is meant to help TNLRP (The New Life RolePlay), so many features may only be available or usable in that community.


## **Boostraping the Project**
This project is solely developed with Python, including many libraries, since it uses mainly the Discord library and many others. For that reason, you'll need to have Python installed together with pip to install the dependencies listed in the *requirements.txt* file.


The following command installs all dependencies: *pip install -r requirements.txt*


**in case some error is showned, be sure to confirm the pip is installed and its $PATH is defined, check this [link](https://pip.pypa.io/en/stable/installation/) for more information.*


## **Contributing**
In order to contribute to this project, you'll need to use the pre-commit hook. All documentation is available at this [link](https://pre-commit.com/).
After installing pre-commit, run *pre-commit install* on a terminal of choice.


The most important rule is to **not**, ever, directly push commits to **master**. Every change must be pull requested and reviewed before making its way to master.


## **Misc. Information**
Cronjob to run "delete_vehicle" script every day
- 0 0 * * * cd /home/nicolau/git/bertram-bot/ && ./cronjob_deletevehicle.py 2>&1 > /tmp/output.log
