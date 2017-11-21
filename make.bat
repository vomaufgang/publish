@ECHO OFF

REM Command file for build automation

REM todo clean, lint, docs, dist (see Make.ps1)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  test          run tests quickly with the default Python
	echo.  test-all      run tests on every Python version with tox
	echo.  lint          check style with flake8
	echo.  cover         check code coverage quickly with the default Python
	echo.  cover-pretty  check code coverage quickly with the default Python
	echo.                and display as an html report in your browser
	echo.  docs          generate Sphinx HTML documentation, including API docs
	echo.  help          display this help message
	goto end
)

if "%1" == "test" (
	python setup.py test
	goto end
)

if "%1" == "test-all" (
	tox
	goto end
)

if "%1" == "lint" (
    pylint apub tests examples setup.py
    goto end
)

if "%1" == "cover" (

	pytest --cov-report term-missing --cov=apub
	goto end
)

if "%1" == "cover-pretty" (
    pytest --cov-report html --cov=apub
    htmlcov\index.html
    goto end
)

if "%1" == "docs" (
    REM Documentation: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
    sphinx-apidoc -o ./docs apub -e -f -T
    cd docs
    make clean
    make html
    cd ..
    if "%2" == "show" (
        docs\_build\html\index.html
    )
    goto end
)

echo.Unrecognized command: '%1'
echo.
echo.Supported commands:
echo.  test, test-all, lint, cover, cover-pretty, docs, help

:end