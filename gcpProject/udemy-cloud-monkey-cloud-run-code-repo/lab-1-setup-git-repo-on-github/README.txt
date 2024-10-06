┌───────────────────────────────────────────────────────────────────────────────────┐
|                           Setup GitHub Repository                                 |
└───────────────────────────────────────────────────────────────────────────────────┘


Go to github.com
Login with your username/password

Click on +New Repository on the top right corner
    Repository Name: udemy-cloud-monkey-cloud-run-code-repo
    Visiblity: Private
    Click on Create repository

Generate Token
	Click on your profile icon
	Click on Settings
	Click on Developer Settings
	Expand Personal Access Tokens
		Click on Tokens(classic)
		Expand Generate New Token
		Click on Generate New Token (Classic)
			Note: local-access-token
			Expiration: No expiration
			Select scopes:
				Check repo
	Click on Generate Token and take a note of the token

Open command prompt and CD into code-root directory
Enter below commands:
    git init
	┌───────────────────────────────────────────────────────────────────────────────────┐
	|     Run these commands only if git cli is not already setup on your machine       |
	|───────────────────────────────────────────────────────────────────────────────────|
	|																					|
	|git config --global user.name "Salim Padela"										|
	|git config --global user.email "salim0630@gmail.com"								|
	|git config credential.helper store													|
	|																					|
	└───────────────────────────────────────────────────────────────────────────────────┘	
    git add .
    git commit -m "initial commit"
    git branch -M main
    git remote add origin git@github.com:SulfredLee/udemy-cloud-monkey-cloud-run-code-repo.git
    git push -u origin main

