djAuction
=========

A Django based web portal for managing auctions

djAuction is intended for the management of small auction events.
The system describes participants in the auction, including their contact information, the items they brought to
be bid upon, and what they won. The system has logic to "check out" a participant, identifying how much money they
owe for their goods, and sharing contact information for donor and winner to exchange what was won. Participants and
items can be associated with auction events and updated as necessary, so if the same people participate in multiple
auction events, their details and purchase histories are saved.

This project was designed to meet the needs of an annual church auction, and for the author to experiment with Django
design strategies. May contain branding that any adopter would need to clean up.

The code was orignally released as a full project, but has recently been reorganized into a portable Django app and re-released. All references to event branding should have been cleaned up (I may have missed some).

Licensed under GLPv3. See LICENSE for more details.

#### Installation Instructions

  - Copy or clone the repository into an existing Django project repository
  - Add the app to the project's INSTALLED_APPS variable in settings.py

    ```
    INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djauction',
    )
    ```
    
  - Make sure the Database settings have been properly configured in settings.py
  - Add the following djAuction specific settings into settings.py for email functionality. Update to use real values.

    ```
    DJAUCTION_SMTP_SERVER = 'smtp.gmail.com'
    DJAUCTION_SMTP_PORT = '587'
    DJAUCTION_SMTP_USER = 'noreply@gmail.com'
    DJAUCTION_SMTP_PASS = 'password'
    ```
    
  - Include the djAuction URLs from some path in the Django project:

    ```
    urlpatterns = patterns('',
    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auction/', include(djauction.urls)),
    )
    ```
    
  - Run **python manage.py syncdb**. Set up an Admin user as needed.
  - Add the following to the static files of the web server (see https://docs.djangoproject.com/en/1.6/howto/static-files)
    - */static/djauction/	/path/to/djauction/static/djauction/*
  - Restart the web server
  - Try accessing the main page of the auction portal at the URL specified above.
