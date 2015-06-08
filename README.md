# Django Testing Tricks

This repository contains a Django project that demonstrates some nifty
Django testing tricks. It was part of a presentation for the Pittsburgh
Code & Supply Django meet-up, June 9, 2015. It was written by Jesse Legg.

# The Kitten apps

`testrick.apps.kittens` contains a Django app that provides an interface
to Reddit Kittens (Kittens-as-a-Service, if you will). There are two views:

 * show-a-kitten: Returns a random kitten image from Reddit's /awww subreddit
 * email-a-kitten: Retrieves a random kitten image and emails it to someone

This app is designed as a basis to demonstrate some testing techniques with
Django and is not an actual SaaS business.

# django-nose

[Nose is nicer testing for Python.](https://nose.readthedocs.org/en/latest/)
It provides extensions to the built-in `unittest` module that make testing
easier and more fun.

[Django-nose](https://pypi.python.org/pypi/django-nose) is a project that
allows you to use nose as the test runner for your Django apps. It offers some
very useful features when it comes to testing Django:

 * Defaults to testing just your project's apps
 * Eliminates the need to import tests into tests/__init__.py
 * Allows you to use [nose plugins](https://nose-plugins.jottit.com/)
 * Bundling of Django fixtures for faster loading
 * Reuse of Django test databases between test runs

Django-nose also adds the ability to run your Django tests through coverage.py
by simply adding `--with-coverage` to the `manage.py test` command.

In this project/presentation, we're simple using Django-nose as our test
runner, but not exploring all that it can do (that is left as an exercise for
the attendee).
