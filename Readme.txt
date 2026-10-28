LITTLE LEMON RESTAURANT API  (Back-end Developer Capstone Project)
===================================================================
Django + Django REST Framework API for the Little Lemon restaurant.
Menu and table-booking endpoints, user registration, token authentication,
MySQL database, unit tests.

SETUP
-----
1. Create the MySQL database:
       CREATE DATABASE reservations;
2. Set your MySQL credentials in littlelemon/settings.py (DATABASES), or export
   DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
   Defaults: name=reservations, user=root, host=127.0.0.1, port=3306.
3. Install dependencies:
       pip install -r requirements.txt
4. Run migrations and start the server:
       python manage.py migrate
       python manage.py createsuperuser
       python manage.py runserver
5. Run the unit tests:
       python manage.py test
   (No MySQL handy? USE_SQLITE=1 python manage.py test)

API PATHS TO TEST  (base URL: http://127.0.0.1:8000)
----------------------------------------------------
Static HTML page (served by Django)
    GET     /restaurant/

User registration and authentication (Djoser)
    POST    /auth/users/                  body: {"username": "...", "password": "..."}
    POST    /auth/token/login/            body: {"username": "...", "password": "..."}
                                          returns {"auth_token": "<token>"}
    POST    /auth/token/logout/           (needs token)
    GET     /auth/users/me/               (needs token)

For every protected request add the header:
    Authorization: Token <auth_token>

Menu API  (GET is public; POST/PUT/PATCH/DELETE need a token)
    GET     /restaurant/menu/             list all menu items
    POST    /restaurant/menu/             body: {"title": "Pasta", "price": "12.50", "inventory": 40}
    GET     /restaurant/menu/<id>         single item
    PUT     /restaurant/menu/<id>         update item
    DELETE  /restaurant/menu/<id>         delete item

Table booking API  (all methods need a token)
    GET     /restaurant/booking/tables/       list bookings
    POST    /restaurant/booking/tables/       body: {"name": "Chetan", "no_of_guests": 4,
                                                     "booking_date": "2026-11-05T19:30:00Z"}
    GET     /restaurant/booking/tables/<id>/  single booking
    PUT     /restaurant/booking/tables/<id>/  update booking
    DELETE  /restaurant/booking/tables/<id>/  delete booking

Admin
    /admin/   (log in with the superuser created above)

TESTING WITH INSOMNIA
---------------------
1. POST /auth/users/ to register, then POST /auth/token/login/ to get a token.
2. In Insomnia choose Auth -> Bearer Token, set the prefix to "Token" and
   paste the token (or add the Authorization header manually).
3. Call the menu and booking endpoints listed above.

UNIT TESTS (restaurant/tests.py)
--------------------------------
Cover the Menu model, serializer, menu CRUD, booking CRUD, authentication
rules, registration + token login, and the static index page.
