# Step 0: install and run development environment
## reference
- [step 0](https://developer.mozilla.org/zh-TW/docs/Learn/Server-side/Django/development_environment)
- [markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)

## use python virtualenv and install django --- in linux
```
source ~/pythonEnv/bin/activate
pip install django
```
## start a new project and run it
```
mkdir django_test
cd django_test
django-admin startproject mytestsite
cd mytestsite
python manage.py runserver
```
# Step 1: Django Local Library example
You can get the source code from here
- [github](https://github.com/mdn/django-locallibrary-tutorial)

# Step 2: Create the skeleton
```
django-admin startproject locallibrary
cd locallibrary
python manage.py startapp catalog
```
## Update timezone
- search for list of tz database time zones
- update it in settings.py

## Prepare the urls.py in application - catalog

## Migration database
```
python manage.py makemigrations
python manage.py migrate
```
# Step 3: Models
- Create models in models.py
```
python manage.py makemigrations
python manage.py migrate
```

# Step 4: Django admin site
- Registering models to admin.py
- Create superuser
 - User: lib_root
 - pw: 1234
 - email: lib_root@test.com
```
python manage.py createsuperuser
```
- You can use listview to adjust the display content in the admin page
