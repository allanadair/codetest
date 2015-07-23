codetest
========

This is a quick and dirty Flask app showcasing some very basic CRUD operations.
It runs on both Python 2 and Python 3.

Directory tree
--------------
.. code::

        .
        ├── README.rst
        ├── codetest
        │   └── __init__.py
        ├── ez_setup.py
        ├── requirements.txt
        ├── setup.py
        └── tests
            └── test_crud_operations.py

Installation
------------
It's just fine to run ``setup.py`` and install the codetest package:

.. code:: bash

        $ ./setup.py install

Or it may be preferable to install to a virtual environment. Here is an example
using pyvenv:

.. code:: bash

        $ pyvenv env
        $ source env/bin/activate
        $ ./setup.py install

To run the unit tests:

.. code:: bash

        $ ./tests/test_crud_operations.py

To run the application in a debug mode:

.. code:: bash

        $ python codetest/__init__.py

To run the application in a production mode (``uwsgi`` is included in the
installation):

.. code:: bash

        $ uwsgi --http-socket :5000 -w codetest:app
