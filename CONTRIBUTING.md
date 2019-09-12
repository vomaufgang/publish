# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/anited/publish/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

### Write Documentation

anited_publish could always use more documentation, whether as part of the
official anited_publish docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/anited/publish/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome. :smiley:

## Get Started!

Ready to contribute? Here's how to set up `anited_publish` for local development.

1. Fork the `anited/publish` repo on GitHub.

2. Clone your fork locally:

   ~~~shell
   $ git clone git@github.com:your_name_here/publish.git
   ~~~

3. Install your local copy into a virtualenv. This is how you set up your fork for local 
   development:

   ~~~shell
   $ cd publish/
   $ python -m venv path_to_your_env && path_to_your_env/Scripts/activate
   $ pip install -e .[dev]
   ~~~

   **Note**: Setup of your virtualenv may differ based on your operating system and whether 
   your Python 3 executable is suffixed as `python3` or not.

   The example above is for Python 3 on Windows.

   `pip install -e .[dev]` installs your local copy as an editable python package and also 
   installs all required development requirements like pylint and pytest.

5. Create a branch for local development:

   ~~~shell
   $ git checkout -b name-of-your-bugfix-or-feature
   ~~~

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass pylint and the tests including
   code coverage:

   ~~~shell
   $ tox
   ~~~

   tox will automatically run all checks against Python 3.6 and 3.7. If your system is 
   missing one of these Python versions you can force tox to run using a specific interpreter 
   version like this:

   ~~~shell
   $ tox -e py36
   ~~~

7. Commit your changes and push your branch to GitHub:

   ~~~shell
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ~~~

8. Submit a pull request through the GitHub website.

   **Note**: Don't forget to add yourself to the list of contributors in AUTHORS.rst. :smiley:

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated.
   Functions and classes should be documented using docstrings.
   Add major features to the list in README.rst.
   Update the readthedocs documentation in /docs.
   
3. The pull request should work for Python >= 3.6. The Azure Pipelines check setup
   in the main repository on GitHub should take care of that. Pull Requests without a or with
   an only partially passing Azure Pipelines check will not be merged.

## Tips

### Testing

To run a subset of tests:

~~~shell
$ pytest tests/test_book.py
~~~


### Makefiles

The repository contains makefiles for all major operating systems  to give
easy access to recurring development tasks such as running tests, building
anited_publish, building the documentation and removing output folders.

You can use the makefile like so:

~~~shell
$ make [command]
~~~

The commands that can be invoked through `make` are the same on
all systems. The most useful for day to day development are:

 * `clean`: removes all temporary build and output directories that may have
   been created during testing or simply running the package (only available on
   *nix operating systems for now)
 * `lint`: runs flake8 on anited_publish and the tests to verify pep8 compliance
 * `test`: runs the test suit against the current python version
 * `test-all`: calls tox to run the test suit against any specified python
   versions
 * `cover`: calculates the test coverage using pytest-cov
 * `docs`: builds and displays the documentation

