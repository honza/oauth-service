OAuth authentication for service-based web applications
=======================================================

Background
----------

This is inspired by the [Flasky Goodness][1] talk given at DjangoCon EU 2012 by
[Kenneth Reitz][2].  He spoke about splitting your massive monolithic Django
application into many single-purpose services.  I was quite intrigued about the
idea and wanted to implement something like that to see how it felt.  The first
issue that I encountered was authentication.  How do you make sure that the
different components share user-related data.  After a brief exchange with
Kenneth on Twitter, I was settled on writing a proof-of-concept OAuth based
authentication system in Python (Django/Flask).

How it works
------------

There are two services:

* Data persistence service
    * Django
    * Authentication
    * Database access
    * Django was chosen because I enjoy its ORM
* Front end service
    * Flask
    * Session
    * HTML rendering (public facing interface)
    * Log in form

Here is a basic flow:

* A user visits the site and is redirected to the login page
* They fill out their username and password
* The front end service sends the username and password to the `/authenticate`
  endpoint of the data persistence service.  If successful, the data layer
  responds with a token and secret.
* The front end service will use the token and secret to make signed OAuth
  requests to the data service.
* The data service knows which clients it will accept requests from.  Each
  service that will connect to the data service will have its own set of
  consumer key and secret.  See the `settings.py` file in the data service.
  You can easily decommission a service (if the gets compromised, etc).
* The two services communicate over HTTP via JSON messages.
* The Django application contains an `oauth_required` view decorator.

Installation
------------

    $ pip install -r requirements.txt

Data service:

    $ cd data/
    $ python manage.py syncdb
    $ python manage.py runserver  # Make sure to create a super user

Log into the admin and create a `User` object under the `data` app.

Front end service:

    $ cd frontend/
    $ python app.py

View the front-end at http://localhost:4444.

Disclaimer
----------

Please note that this was written as a proof-of-concept.  Use it as an example
of how you might write something like this.  It would probably work fine in
production but I would carefully consider all the security-related concerns
before continuing.

License
-------

BSD, short and sweet

[1]: http://klewel.com/conferences/djangocon-2012/index.php?talkID=44
[2]: https://github.com/kennethreitz
