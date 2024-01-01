# kivy-gui-To-Do-list
#Pacakage Requirements: **kivy, datetime**

#Package Installation

Before Kivy can be installed, Python and pip needs to be pre-installed. Then, start a new terminal that has Python available. In the terminal, update pip and other installation dependencies so you have the latest version as follows (for linux users you may have to substitute python3 instead of python and also add a --user flag in the subsequent commands outside the virtual environment):

**python -m pip install --upgrade pip setuptools virtualenv**

Create virtual environment¶
Create a new virtual environment for your Kivy project. A virtual environment will prevent possible installation conflicts with other Python versions and packages. It’s optional but strongly recommended:

Create the virtual environment named kivy_venv in your current directory:

**python -m virtualenv kivy_venv**

Activate the virtual environment. You will have to do this step from the current directory every time you start a new terminal. This sets up the environment so the new kivy_venv Python is used.

For Windows default CMD, in the command line do:

**kivy_venv\Scripts\activate**

If you are in a bash terminal on Windows, instead do:

**source kivy_venv/Scripts/activate**

If you are in linux or macOS, instead do:

**source kivy_venv/bin/activate**

Your terminal should now preface the path with something like (kivy_venv), indicating that the kivy_venv environment is active. If it doesn’t say that, the virtual environment is not active and the following won’t work.

For more details, read the official documentation here
https://kivy.org/doc/stable/
