## Why we have this tool
This is a tool to create and maintain software project.

## How to use this tool
1. Installation
  - Download this project to ~/Documents/bin/
  - Run the installation script `bash ~/Documents/bin/projectManager/install_manager.sh`
1. Run the bash script
  - `cd <to your project folder>`
  - `projectManager.sh`
1. Select what you want to create
1. DONE

## Example --- Create cpp normal project

```bash
$ projectManager.sh 
============ Welcome to /home/user/bin/projectManager/projectManager.sh ============
============ Action Select ============
0. Create Project
1. Update Project
>=2. quit
User selection: 0
Create Project
============ Language Select ============
0. Python
1. Cpp
>=2. quit
User selection: 1
Project Name: tt
New project name: tt
Cpp
============ Project Select ============
0. Cpp General Project
1. Cpp QT Project
>=2. quit
User selection: 0


Action: Create Project
Language: Cpp
Project: Cpp General Project
user call script from: /home/user/cpp/app/temp_testing
Updating dependencies
Resolving dependencies... (0.7s)

No dependencies to install or update
2022-11-13 12:17:43,433 [INFO] [project_manager] [main.py:main:42] [MainThread] We get args: Namespace(action='Create Project', lang='Cpp', projectName='tt', projectPath='/home/user/cpp/app/temp_testing', projectType='Cpp General Project')
2022-11-13 12:17:43,433 [INFO] [project_manager] [cppCreator.py:__create_general_project:32] [MainThread] Creating project in folder: /home/user/cpp/app/temp_testing
/home/user/cpp/app/temp_testing
```
