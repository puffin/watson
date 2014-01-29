Watson
======

Watson is a continuous unit test runner for django. As long as the script is running, it will monitor for changes in your code and re-run your test suite when needed.

Features
--------

* Monitor source code and run tests on change
* OSX notifications
* Colored test output

Installation
------------

Watson can be installed from PyPI using easy_install::
    
    $ easy_install Watson
    
or pip::
    
    $ pip install Watson

Setup
-----

To setup Watson under Django add ``watson`` to your ``INSTALLED_APPS`` setting.
The run ``manage.py watson`` to start the tester process. You can give an
application label or test name using the same format as the built-in ``test``
command.