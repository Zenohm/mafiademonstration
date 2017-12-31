Mafia Demonstration
===================

A user friendly interface for playing a simplified game of Mafia.

----


Requirements
------------

To run "Mafia Demonstration" you will need `Kivy`_, `Click`_, and the circular layout library from Kivy's garden.

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

Use the make tool to automatically install all dependencies required for the project:

.. code-block:: bash

    $ make dependencies


Usage
-----

Launch the app via:

.. code-block:: bash

    $ make run

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
.. _`Click`: https://github.com/pallets/click
.. _`Cython`: https://pypi.python.org/pypi/Cython/
.. _`Kivy`: https://github.com/kivy/kivy
.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`Sphinx`: http://sphinx-doc.org/
.. _`file an issue`: https://github.com/zenohm/mafiademonstration/issues
.. _`pytest-cov`: https://pypi.python.org/pypi/pytest-cov
.. _`pytest`: http://pytest.org/latest/
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.org/en/latest/
