# CRM-Epic-Event

## Table of contents

1. [General info](#1-general-info)
2. [Technologies](#2-technologies)
3. [Setup](#3-setup)
    - [Setup for Unix](#a-setup-for-unix)
    - [Setup for Windows](#b-setup-for-windows)
4. [Author](#4-author)

## 1. General info
CRM-Epic-event-main is a secured Customer Relationship Management system made with Django REST. 

[Documentation for CRM Epic Event](https://documenter.getpostman.com/view/18470677/UVeDtTUR)

## 2. Technologies

Python 3.10.0

* asgiref==3.4.1
* autopep8==1.6.0
* backports.zoneinfo==0.2.1
* Django==4.0.1
* django-filter==21.1
* djangorestframework==3.13.1
* drf-nested-routers==0.93.4
* importlib-metadata==4.10.1
* Markdown==3.3.6
* psycopg2-binary==2.9.3
* pycodestyle==2.8.0
* pytz==2021.3
* sqlparse==0.4.2
* toml==0.10.2
* zipp==3.7.0

## 3. Setup
### A) *Setup for Unix*

Only first-time use :
After downloading CRM-Epic-event-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, download it from [here](https://github.com/ValentinPhB/CRM-Epic-Event).

Create a virtual environment in "PATH" and install packages from requirements.txt.
```
$ cd ../path/to/CRM-Epic-event-main
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements.txt
```

Create postgresql database :
```
$ sudo su postgres
$ psql postgres

postgres= $ CREATE DATABASE auth;

postgres= $ CREATE ROLE django_auth WITH LOGIN PASSWORD 'valval';

postgres= $ GRANT ALL PRIVILEGES ON DATABASE auth TO django_auth;
```
#### *Migrations* :
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

#### *Run local server for Unix* 
```
$ python3 manage.py runserver
```

Ubuntu :
Use alt + click on http:// adresse.

Mac :
Use option + click on http:// adresse.

Create Superuser :
```
$ python3 manage.py createsuperuser
```

FOLLOW THE DOCUMENTATION :

[Documentation for CRM Epic Event](https://documenter.getpostman.com/view/18470677/UVeDtTUR)

### B) *Setup for Windows* 

Only first-time use :
After downloading CRM-Epic-event-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, download it from [here](https://github.com/ValentinPhB/CRM-Epic-Event).

Create a virtual environment in "PATH" and install packages from requirements.txt.

Then, using cmd, go to "PATH", create a virtual environment and install packages from requirements.txt.

```
$ CD ../path/to/P10_SoftDesk_API
$ py -m venv env
$ env\Scripts\activate.bat
$ py -m pip install -U pip
$ pip install -r requirements.txt
```

Create postgresql database :
[Installation for windows OS](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm)

Then :
```
# COMMENT: CREATE DATA BASE
postgres= $ CREATE DATABASE auth;

# CREATE django_auth
postgres= $ CREATE ROLE django_auth WITH LOGIN PASSWORD 'valval';

# Give django_auth a superuser statu
postgres= $ GRANT ALL PRIVILEGES ON DATABASE auth TO django_auth;
```
#### *Migrations* :
```
$ python manage.py makemigrations
$ python manage.py migrate
```

#### *Run local server for Windows*
```
$ python manage.py runserver
```
Use alt + click on http:// adresse.

Create Superuser :
```
$ python manage.py createsuperuser
```

FOLLOW THE DOCUMENTATION :

[Documentation for CRM Epic Event](https://documenter.getpostman.com/view/18470677/UVeDtTUR)

## 4. Author

Valentin Pheulpin
