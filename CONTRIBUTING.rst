============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
======================

Report Bugs
-----------

Report bugs at https://github.com/vomaufgang/apub/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
--------

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
------------------

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
-------------------

apub could always use more documentation, whether as part of the 
official apub docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
---------------

The best way to send feedback is to file an issue at https://github.com/vomaufgang/apub/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
============

Ready to contribute? Here's how to set up `apub` for local development.

1. Fork the `apub` repo on GitHub.

2. Clone your fork locally::

    $ git clone git@github.org:your_name_here/apub.git

3. Install your local copy into a virtualenv. This is how you set up your fork for local development::

    $ python -m venv path_to_your_env && path_to_your_env/Scripts/activate
    $ cd apub/
    $ pip install -e .

.. note:: Setup of your virtualenv may differ based on your operating system and whether your Python 3 executable is suffixed as `python3` or not.

  The example above is for Python 3 on Windows.

4. Install development requirements like flake8 and pytest::

    $ pip install -r requirements.txt

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature
   
   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 apub tests
    $ pytest apub tests
    $ tox

  Check the code coverage of your changes and unit tests::

   $ pytest --cov=apub tests

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
=======================

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
   Functions and classes should be documented using docstrings.
   Add major features to the list in README.rst.
   Update the readthedocs documentation in /docs.
3. The pull request should work for Python >= 3.6. Check
   https://travis-ci.org/vomaufgang/apub/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
====

Testing
-------

To run a subset of tests::

	$ pytest tests/test_apub.py

Documentation
-------------

The documentation is tailored to the readthedocs theme. The theme is part of the
requirements, so if you pip installed those before using `pip install -r requirements.txt`
you are good to go.

.. note:: If the theme is not installed `make docs` will fall back to the
   default sphinx theme.

Makefiles
---------

The repository contains makefiles for all major operating systems  to give
easy access to recurring development tasks such as running tests, building
apub, building the documentation and removing output folders.

You can use the makefile like so::

    make [command]

The commands that can be invoked through `make` are the same on
all systems. The most useful for day to day development are:

 * `clean`: removes all temporary build and output directories that may have
   been created during testing or simply running the package
 * `lint`: runs flake8 on apub and the tests to verify pep8 compliance
 * `test`: runs the test suit against the current python version
 * `test-all`: calls tox to run the test suit against any specified python
   versions
 * `coverage`: calculates the test coverage using pytest-cov
 * `docs`: builds and displays the documentation

