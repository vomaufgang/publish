@ECHO OFF

REM Command file for build automation

REM todo clean, lint, docs, dist (see Make.ps1)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  test          run tests quickly with the default Python
	echo.  test-all      run tests on every Python version with tox
	echo.  lint          check style with pylint
	echo.  cover         check code coverage quickly with the default Python
	echo.  cover-pretty  check code coverage quickly with the default Python
	echo.                and display as an html report in your browser
	echo.  dist          package
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
    pylint publish tests examples setup.py
	flake8 publish tests examples setup.py
    goto end
)

if "%1" == "cover" (
	pytest --cov-report term-missing --cov=publish tests/
	goto end
)

if "%1" == "cover-pretty" (
    pytest --cov-report html --cov=publish
    htmlcov\index.html
    goto end
)

if "%1" == "dist" (
	del dist\*.* /F /Q
	python setup.py sdist
	python setup.py bdist_wheel
	dir dist
	goto end
)

echo.Unrecognized command: '%1'
echo.
echo.Supported commands:
echo.  test, test-all, lint, cover, cover-pretty, dist, help

:end
