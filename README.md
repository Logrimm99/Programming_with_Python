# Python Project for the Module: Programming with Python
Contains both the project assignment, as well as the code segments from the written assignment.

## Setup Guide of the Project for Python3.12
### 1. Move to path where the project shall be cloned and execute:
  

    git clone https://github.com/Logrimm99/Programming_with_Python.git

### 2. Install pip for Python3.12:
		

##### Note: might vary slightly depending on the CLI
		
    python -m ensurepip --upgrade


### 3. Install required modules: 
 ##### Before installing the modules, it might be necessary to install the setuptools module or Microsoft Visual C++ first
    pip install --upgrade setuptools

 ##### If in main folder of project:
 
    python3 -m pip install -r requirements.txt
  
 ##### or, if not in project folder:
	
    python3 -m pip install -r <pathToProject>/requirements.txt


### 4. To run main file:
  ##### If in project folder:
    python3 Programming_with_Python.py
  ##### If not in project folder:
    python3 <pathToProject>/Programming_with_Python.py


### 5. To run unittests:
  ##### If in project folder:
    python3 -m unittest Programming_with_Python.py
  ##### If not in project folder:
    python3 -m unittest path_to_project_folder/Programming_with_Python.py


### 6. To commit changes:
  ##### Select what should be commited:
    git add <filename>
  ##### or:
    git add *

###### Commit the changes:
    git commit -m "<Commit message>"

### 7. To push the commit:
  ##### To push to the develop branch:
    git push origin develop
  ##### To push to another branch:
   ##### Make sure you are working on the branch
    git push origin <branchname>

### 8. To pull changes:
  
    git pull

### 9. Merge remote changes from another branch:
  

    git merge <branchname>

### 10. Checkput specific branch:
  

    git checkout <branchname>
