Mafia Demonstration
===================

A user friendly interface for playing a simplified game of Mafia.

----


Features
--------

* Minimal design with flat colors
* Text labels that contain clickable links
* Several slides that can be controlled via swipe gestures
* Settings panel to change the slider transition delay (``<F1>``)


Requirements
------------

To run "Mafia Demonstration" you only need `Kivy`_.

Depending on the features that you want to use, you do require additional libs though.

* `pytest`_ - implement readable tests without boilerplate-code
* `pytest-cov`_ - generate an ``html`` coverage report
* `Sphinx`_ - generate a readable ``html`` documentation
* `Buildozer`_ - deploy your app to an Android mobile device


Installation
------------

Clone the repository:

.. code-block:: bash

    $ git clone https://github.com/zenohm/mafiademonstration.git
    $ cd mafiademonstration


Install the app package in "editable" mode:

.. code-block:: bash

    $ python setup.py develop

Install Kivy's garden tool and the required packages.


.. code-block:: bash

    $ python -m pip install kivy-garden
    $ garden install <module name>

.. note:: You can find the required garden packages listed in the kivy-requirements file:



Usage
-----

Launch the app via:

.. code-block:: bash

    $ python mafiademonstration

Run the `pytest`_ test suite:

.. code-block:: bash

    $ make test

Generate an ``html`` coverage report and open it:

.. code-block:: bash

    $ make coverage

Generate `Sphinx`_ ``html`` documentation and open it:

.. code-block:: bash

    $ make docs

Build an android apk with `Buildozer`_:

.. code-block:: bash

    $ make apk

Deploy the app to your android device with `Buildozer`_:

.. code-block:: bash

    $ make deploy


License
-------

Distributed under the terms of the `MIT license`_, "Mafia Demonstration" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


.. _`@hackebrot`: https://github.com/hackebrot
.. _`Buildozer`: https://github.com/kivy/buildozer
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`Cookiedozer`: https://github.com/hackebrot/cookiedozer
.. _`Cython`: https://pypi.python.org/pypi/Cython/
.. _`Kivy`: https://github.com/kivy/kivy
.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`Sphinx`: http://sphinx-doc.org/
.. _`file an issue`: https://github.com/zenohm/mafiademonstration/issues
.. _`pytest-cov`: https://pypi.python.org/pypi/pytest-cov
.. _`pytest`: http://pytest.org/latest/
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.org/en/latest/
