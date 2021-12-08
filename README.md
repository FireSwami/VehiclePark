# Car Park

Car Park is an API for maintaining (sorting, editing, deleting, displaying)
a database of drivers and vehicles.

### Installation

Use ***SETUP*** instructions.


### Usage

Use **[swagger](http://127.0.0.1:8000/swagger/)**, 
**[redoc](http://127.0.0.1:8000/redoc/)**,
**[postman](https://www.postman.com/)**
or ***direct links from task***
**[forexample](http://127.0.0.1:8000/drivers/driver/)**
to get info from API.
Also added sorting for comfortable view DBs elements.


### Requirements
+ Python version> = 3.9.0
+ Framework - Django> = 3.2.8
+ Database - SQLite

### Addons
+ The project has tests to control the work.
  
    >#### python manage.py test

+ The project has **[Django admin panel](http://127.0.0.1:8000/admin/)**
  for the convenience of filling and maintaining the database
  (you must create and use own username, password; use ***SETUP*** instructions.)

+ Sorting and formatting by ***flake8 / black / isort*** 
  were applied to improve the code quality. If you need install it try:
  
    >#### pip install -r dev.txt