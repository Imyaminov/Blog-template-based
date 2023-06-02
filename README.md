# Blog Application

This is my template based Blog website built with monolithic approach using Django and Javascript.

## Description

This Django project contains Custom authorization, login/logout, password set/reset, recommendation and tagging system. Moreover users can also comment out to posts.
For search system, PostgreSQL full text search is implemented with search headline and ranking capabilities. Also Redis is used to cache some pages and different query optimization techniques
is used to reach good performance.

## Getting Started

### Dependencies

* All dependencies and prereqisities can be found in [requirements.txt](https://github.com/Imyaminov/blog-app-template-based/blob/main/requirements.txt) file of main project directory

### Installing

* clone the repo 
  ```sh
  git clone https://github.com/Imyaminov/blog-app-template-based.git
  ```
  
### Executing program
* configure the database. By default django uses sqlite3 but this project requires [PostgreSQL](https://www.postgresql.org/download/) database because of search engine. you can open local_settings.py file or directly configure in [settings.py](https://github.com/Imyaminov/blog-app-template-based/blob/main/core/settings.py) 
* install requirements:
```
 pip install -r requirements.txt
```
* makemigrations to create migration files:
```
 python manage.py makemigrations
```
* then migrate to apply those migrations:
```
python manage.py migrate
```
* finally run the server:
```
python manage.py runserver
```

** ! run "python manage.py createsuperuser" to create superuser to access the admin page

## Help

Any advise for common problems or issues contact [me](250503iaa@gmail.com).

## Authors

Contributors names and contact info
  
ex. [Abduboriy](https://www.linkedin.com/in/abduboriy-imyaminov/)


## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
