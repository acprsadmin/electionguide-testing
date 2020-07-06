## Election Guide Website

[![CircleCI](https://circleci.com/gh/IFES1987/electionguide.svg?style=svg&circle-token=e422ac031b0eb151ea2761548fbe081764d5f22c)](https://circleci.com/gh/IFES1987/electionguide)

A django-powered website (http://www.electionguide.org)

### Development

Install the requirements

    $ pip install -r requirements.txt

To setup the local database:

    $ python manage.py syncdb
    $ python manage.py migrate

To run the app

    $ python manage.py runserver

### Deployment

`master` branch is automatically deployed to Heroku.

### Manual Deployment to Heroku

Run these commands to deploy the project to Heroku:

```
    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups:auto-month
    heroku addons:add memcachier:dev
    heroku pg:promote DATABASE_URL
    heroku config:set DJANGO_CONFIGURATION=Production
    heroku config:set DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku open
```


### Settings

For configuration purposes, the following table maps the 'eguide' environment variables to their Django setting:

|Environment Variable                    |Django Setting              |Development Default          |Production Default
| -------------------------------------- | -------------------------- | --------------------------- | -----------------
|DJANGO_AWS_ACCESS_KEY_ID                |AWS_ACCESS_KEY_ID           |n/a                          |raises error
|DJANGO_AWS_SECRET_ACCESS_KEY            |AWS_SECRET_ACCESS_KEY       |n/a                                            |raises error
|DJANGO_AWS_STORAGE_BUCKET_NAME          |AWS_STORAGE_BUCKET_NAME     |n/a                                            |raises error
|DJANGO_DATABASES                        |DATABASES                   |See code                                       |See code
|DJANGO_DEBUG                            |DEBUG                       |True                                           |False
|DJANGO_CONFIGURATION                    |DJANGO_CONFIGURATION               |Development |Production
|DJANGO_SECRET_KEY                       |SECRET_KEY                  |CHANGEME!!!                                    |raises error
|DJANGO_EMAIL_HOST_PASSWORD        |EMAIL_HOST_PASSWORD   |n/a                                       |raises error
|DJANGO_EMAIL_HOST_USER              |EMAIL_HOST_USER:         |n/a                                  |raises error
|DJANGO_MAILGUN_API_KEY      |MAILGUN_API_KEY |n/a                                            |raises error
|DJANGO_RECAPTCHA_PRIVATE_KEY                |RECAPTCHA_PRIVATE_KEY          |raises error                  |raises error
|DJANGO_RECAPTCHA_PUBLIC_KEY                |RECAPTCHA_PUBLIC_KEY          |raises error                  |raises error
