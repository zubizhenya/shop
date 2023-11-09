# Django store
This is an online store that I am writing in Python using the Django framework, I am learning new tools and
I integrate them into the online store.

## Installation

* You must copy all the contents of the repository to a separate directory.

* Enter the following. commands in the terminal from the project folder:

```
python manage.py makemigrations
python manage.py migrate
```

* After this you need to create a superuser with the command:

```
python manage.py createsuperuser


* Launch the site using the command:

...
python manage.py runserver

* Now you can go to the main page of the project at `http://127.0.0.1:8000/bboard/`.
* On the site you can: register new users, create/edit/delete products for sale,
  comment on products, create categories for products, search for products by category, 
  name, date of creation. I also created pagination for the product on the site. 
  But before using the site’s tools, you need to log in.
