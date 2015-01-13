============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/vomaufgang/apub/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

apub could always use more documentation, whether as part of the 
official apub docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/vomaufgang/apub/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `apub` for local development.

1. Fork the `apub` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@bitbucket.org:your_name_here/apub.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv apub
    $ cd apub/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature
   
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 apub tests
    $ python setup.py test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv. 

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.3 and 3.4, and for PyPy. Check
   https://travis-ci.org/vomaufgang/apub/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

Testing
~~~~~~~

To run a subset of tests::

	$ python -m unittest tests.test_apub

Documentation
~~~~~~~~~~~~~

The documentation is tailored to the readthedocs theme. `pip install` the
theme into your virtualenv to use it for your own builds of the documentation::

    pip install rtd_sphinx_theme

.. note:: If the theme is not installed `make docs` will fall back to the
   default sphinx theme.

Makefiles
~~~~~~~~~

The repository contains makefiles to give easy access to recurring
development tasks such as running tests, building apub, building the
documentation and removing output folders.

Unix/Linux/Mac users can use the traditional makefile like so::

    make [command]

Windows users can use the PowerShell makefile from within a PowerShell session
like so::

    .\Make [command]

.. note:: Windows users may have to set their PowerShell execution-policy to
   remote-signed before PowerShell allows the execution of self-written
   PowerShell scripts. While tinkering with the execution-policy on a
   development machine is usually fine, **do not** change this setting in a
   production environment.

The commands that can be invoked through `make` or `\Make` are the same on
all systems. The most useful for day to day development are:

 * `clean`: removes all temporary build and output directories that may have
   been created during testing or simply running the package
 * `lint`: runs flake8 on apub and the tests to verify pep8 compliance
 * `test`: runs the test suit against the current python version
 * `test-all`: calls tox to run the test suit against any specified python
   versions
 * `coverage`: calculates the test coverage using nosetests
 * `docs`: builds and displays the documentation

